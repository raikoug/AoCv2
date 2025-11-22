from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Set, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Grid = List[str]
Pos = Tuple[int, int]
Region = Set[Pos]

# Direzioni ortogonali
DIRS: Tuple[Pos, ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# --- Helpers di base ------------------------------------------------------


def parse_grid(raw: str) -> Grid:
    return [line.rstrip("\n") for line in raw.splitlines() if line.strip()]


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def neighbors(grid: Grid, r: int, c: int) -> Iterable[Pos]:
    rows, cols = len(grid), len(grid[0])
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc, rows, cols):
            yield nr, nc


def find_regions(grid: Grid) -> List[Region]:
    """
    Trova tutte le regioni connesse di stesso carattere.
    Ogni regione è un set di posizioni (r, c).
    """
    rows, cols = len(grid), len(grid[0])
    visited: Region = set()
    regions: List[Region] = []

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue

            char = grid[r][c]
            region: Region = set()
            stack: List[Pos] = [(r, c)]
            visited.add((r, c))

            while stack:
                cr, cc = stack.pop()
                region.add((cr, cc))

                for nr, nc in neighbors(grid, cr, cc):
                    if (nr, nc) in visited:
                        continue
                    if grid[nr][nc] != char:
                        continue
                    visited.add((nr, nc))
                    stack.append((nr, nc))

            regions.append(region)

    return regions


# --- Parte 1: perimetro (fences) -----------------------------------------


def perimeter_of(region: Region) -> int:
    """
    Perimetro di una regione:
    per ogni cella, contiamo i lati che non toccano un'altra cella della regione.
    """
    perim = 0
    for r, c in region:
        for dr, dc in DIRS:
            if (r + dr, c + dc) not in region:
                perim += 1
    return perim


# --- Parte 2: numero di "sides" (lati) -----------------------------------


def count_sides_of(region: Region) -> int:
    """
    Calcola il numero di lati (sides) di una regione, come da testo del puzzle.

    È la tua stessa funzione, adattata a lavorare direttamente su set[(r, c)].
    """
    reg = region

    left: set[Pos] = set()
    right: set[Pos] = set()
    up: set[Pos] = set()
    down: set[Pos] = set()

    for (r, c) in reg:
        if (r - 1, c) not in reg:
            up.add((r, c))
        if (r + 1, c) not in reg:
            down.add((r, c))
        if (r, c + 1) not in reg:
            right.add((r, c))
        if (r, c - 1) not in reg:
            left.add((r, c))

    corners = 0
    # upper corners
    for (r, c) in up:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r - 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r - 1, c + 1) in left and (r, c) not in right:
            corners += 1

    # lower corners
    for (r, c) in down:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r + 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r + 1, c + 1) in left and (r, c) not in right:
            corners += 1

    return corners


# --- Soluzioni richieste dal template ------------------------------------


def solve_1(test_string: str | None = None) -> int:
    """
    Prezzo = area * perimetro per ogni regione, somma totale.
    """
    inputs_1 = GI.input if test_string is None else test_string
    grid = parse_grid(inputs_1)

    regions = find_regions(grid)

    total = 0
    for region in regions:
        area = len(region)
        perim = perimeter_of(region)
        total += area * perim

    return total


def solve_2(test_string: str | None = None) -> int:
    """
    Prezzo = area * numero di lati (sides) per ogni regione, somma totale.
    """
    inputs_1 = GI.input if test_string is None else test_string
    grid = parse_grid(inputs_1)

    regions = find_regions(grid)

    total = 0
    for region in regions:
        area = len(region)
        sides = count_sides_of(region)
        total += area * sides

    return total


if __name__ == "__main__":
    test_1 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    test_2 = """AAAA
BBCD
BBCC
EEEC"""
    test_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
    test_4 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

    # Input reale da AOC
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test veloci:
    # print(f"Part 1 (test_1): {solve_1(test_1)}")
    # print(f"Part 2 (test_1): {solve_2(test_1)}")
    # print(f"Part 1 (test_2): {solve_1(test_2)}")
    # print(f"Part 2 (test_2): {solve_2(test_2)}")
    # print(f"Part 1 (test_3): {solve_1(test_3)}")
    # print(f"Part 2 (test_3): {solve_2(test_3)}")
    # print(f"Part 1 (test_4): {solve_1(test_4)}")
    # print(f"Part 2 (test_4): {solve_2(test_4)}")
