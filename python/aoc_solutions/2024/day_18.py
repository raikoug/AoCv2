from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import List, Tuple

import sys

import numpy as np

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Pos = Tuple[int, int]  # (x, y) = (col, row)


# ---------------------------------------------------------------------------
# Helpers comuni
# ---------------------------------------------------------------------------

def in_boundaries(p: Pos, size: int) -> bool:
    x, y = p
    return 0 <= x < size and 0 <= y < size


def build_grid(raw: str, size: int, corrupted_count: int) -> np.ndarray:
    """
    Costruisce una griglia `size x size` con:
    - 0 = cella libera
    - 1 = byte corrotto (ostacolo)
    usando i primi `corrupted_count` byte dell'input.
    """
    grid = np.zeros((size, size), dtype=np.uint8)
    lines = [ln for ln in raw.splitlines() if ln.strip()]

    for line in lines[:corrupted_count]:
        x_str, y_str = line.split(",")
        x = int(x_str)
        y = int(y_str)
        grid[y, x] = 1

    return grid


def navigate_grid(grid: np.ndarray, start: Pos, end: Pos) -> int:
    """
    BFS su griglia NumPy.
    Restituisce il numero di passi del percorso minimo, oppure -1 se non esiste.
    """
    size = grid.shape[0]
    sx, sy = start
    ex, ey = end

    if grid[sy, sx] == 1 or grid[ey, ex] == 1:
        return -1

    q: deque[Tuple[Pos, int]] = deque()
    q.append(((sx, sy), 0))
    visited: set[Pos] = {(sx, sy)}

    while q:
        (x, y), steps = q.popleft()

        if (x, y) == (ex, ey):
            return steps

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (
                in_boundaries((nx, ny), size)
                and grid[ny, nx] == 0
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                q.append(((nx, ny), steps + 1))

    return -1


def shortest_path_after_n_bytes(raw: str, size: int, corrupted_count: int) -> int:
    grid = build_grid(raw, size, corrupted_count)
    start: Pos = (0, 0)
    end: Pos = (size - 1, size - 1)
    return navigate_grid(grid, start, end)


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None, corrupted_bytes: int | None = None) -> int:
    """
    Restituisce la lunghezza del percorso minimo dopo che sono caduti i primi
    `corrupted_bytes` byte:
    - input reale: default 1024
    - test: di default 12 (valore del sample AoC)
    """
    raw = GI.input if test_string is None else test_string
    is_test = test_string is not None

    size = 7 if is_test else 71

    if corrupted_bytes is None:
        corrupted_bytes = 12 if is_test else 1024

    return shortest_path_after_n_bytes(raw, size, corrupted_bytes)


# ---------------------------------------------------------------------------
# Part 2
# ---------------------------------------------------------------------------

def solve_2(test_string: str | None = None) -> str:
    """
    Trova il PRIMO byte (coordinata "x,y") la cui caduta rende impossibile
    raggiungere il traguardo.
    """
    raw = GI.input if test_string is None else test_string
    is_test = test_string is not None

    size = 7 if is_test else 71

    lines = [ln for ln in raw.splitlines() if ln.strip()]
    total_bytes = len(lines)

    min_corrupted = 12 if is_test else 1024

    lo = min_corrupted
    hi = total_bytes
    ans: int | None = None

    while lo <= hi:
        mid = (lo + hi) // 2
        dist = shortest_path_after_n_bytes(raw, size, mid)
        if dist == -1:
            # già bloccato con mid byte -> prova a vedere se si blocca prima
            ans = mid
            hi = mid - 1
        else:
            # ancora raggiungibile -> servono più byte corrotti
            lo = mid + 1

    if ans is None:
        raise RuntimeError("Non ho trovato un numero di byte che blocchi il percorso.")

    # ans è il numero MINIMO di byte che blocca il percorso.
    # Il byte "responsabile" è quello in posizione ans-1 (0-based).
    return lines[ans - 1]


if __name__ == "__main__":
    test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    print("Test Part 1 (12 bytes):", solve_1(test, corrupted_bytes=12))
    print("Test Part 2 (sample):", solve_2(test))

    print("Part 1 (input reale):", solve_1())
    print("Part 2 (input reale):", solve_2())
