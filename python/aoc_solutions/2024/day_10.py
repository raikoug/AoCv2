from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Grid = List[List[int]]
Pos = Tuple[int, int]


# --- Helpers comuni -------------------------------------------------------


def parse_grid(raw: str) -> Grid:
    return [
        [int(ch) for ch in line.strip()]
        for line in raw.splitlines()
        if line.strip()
    ]


def possible_next_steps(pos: Pos, grid: Grid) -> List[Pos]:
    row, col = pos
    current_height = grid[row][col]

    candidates: List[Pos] = [
        (row + 1, col),
        (row, col + 1),
        (row - 1, col),
        (row, col - 1),
    ]

    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    good: List[Pos] = []
    for nr, nc in candidates:
        if (
            0 <= nr <= max_row
            and 0 <= nc <= max_col
            and grid[nr][nc] == current_height + 1
        ):
            good.append((nr, nc))

    return good


def find_trailheads(grid: Grid) -> List[Pos]:
    return [
        (r, c)
        for r, row in enumerate(grid)
        for c, val in enumerate(row)
        if val == 0
    ]


def score_trailhead(grid: Grid, start: Pos) -> int:
    """
    Parte 1: per un trailhead, conta il numero di picchi (celle con 9)
    distinti raggiungibili.
    """
    stack: List[Pos] = [start]
    visited: set[Pos] = set()
    peaks: set[Pos] = set()

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if grid[r][c] == 9:
            peaks.add((r, c))
            continue

        for nxt in possible_next_steps((r, c), grid):
            if nxt not in visited:
                stack.append(nxt)

    return len(peaks)


def rating_trailhead(grid: Grid, start: Pos) -> int:
    """
    Parte 2: per un trailhead, conta il numero di percorsi distinti
    che portano a un picco (cella con 9).

    Non usiamo visited perché i valori aumentano da 0 a 9:
    non ci sono cicli (cammino sempre strettamente crescente).
    """
    stack: List[Pos] = [start]
    rating = 0

    while stack:
        r, c = stack.pop()

        if grid[r][c] == 9:
            rating += 1
            continue

        for nxt in possible_next_steps((r, c), grid):
            stack.append(nxt)

    return rating


# --- Soluzioni richieste dal template -------------------------------------


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    grid = parse_grid(inputs_1)
    trailheads = find_trailheads(grid)
    return sum(score_trailhead(grid, th) for th in trailheads)


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    grid = parse_grid(inputs_1)
    trailheads = find_trailheads(grid)
    return sum(rating_trailhead(grid, th) for th in trailheads)


if __name__ == "__main__":
    test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    test_2 = """012345
123456
234567
345678
416789
567891
"""

    # Input reale da AOC
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test veloci:
    # print(f"Part 1 (test): {solve_1(test)}")
    # print(f"Part 2 (test): {solve_2(test)}")
    # print(f"Part 1 (test_2): {solve_1(test_2)}")
    # print(f"Part 2 (test_2): {solve_2(test_2)}")
