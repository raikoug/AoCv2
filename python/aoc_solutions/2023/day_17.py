from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Dict
import heapq
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


Coord = tuple[int, int]
State = tuple[int, int, int, int]  # (row, col, dir, run)


def _parse_grid(raw: str) -> list[list[int]]:
    return [[int(ch) for ch in line.strip()] for line in raw.splitlines() if line.strip()]


#                 U        R        D        L
DIRS: tuple[Coord, ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _dijkstra(
    grid: list[list[int]],
    min_run: int,
    max_run: int,
) -> int:
    rows = len(grid)
    cols = len(grid[0])

    # priority queue items: (cost, row, col, dir, run)
    pq: list[tuple[int, int, int, int, int]] = []
    # dir = 0..3, run = steps consecutivi in questa direzione
    # dir = -1 significa "nessuna direzione ancora"
    heapq.heappush(pq, (0, 0, 0, -1, 0))

    best: Dict[State, int] = {}

    target: Coord = (rows - 1, cols - 1)

    while pq:
        cost, r, c, d, run = heapq.heappop(pq)

        if (r, c) == target and (d == -1 or run >= min_run):
            # Possiamo fermarci solo se l'ultimo segmento rispetta min_run
            return cost

        state: State = (r, c, d, run)
        old = best.get(state)
        if old is not None and old <= cost:
            continue
        best[state] = cost

        for nd, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if d == -1:
                # Prima mossa: inizio segmento di lunghezza 1
                nrun = 1
            elif nd == d:
                # Proseguo diritto
                nrun = run + 1
            else:
                # Curva: consentita solo se il segmento precedente ha già min_run passi
                if run < min_run:
                    continue
                nrun = 1

            if nrun > max_run:
                continue

            ncost = cost + grid[nr][nc]
            nstate: State = (nr, nc, nd, nrun)
            old = best.get(nstate)
            if old is None or ncost < old:
                heapq.heappush(pq, (ncost, nr, nc, nd, nrun))

    raise RuntimeError("No path found")


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = _parse_grid(raw)
    # Parte 1: max 3 in fila, puoi girare dopo almeno 1 passo
    return _dijkstra(grid, min_run=1, max_run=3)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = _parse_grid(raw)
    # Parte 2: ultra crucible: segmenti di 4–10 passi
    return _dijkstra(grid, min_run=4, max_run=10)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
