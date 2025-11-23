from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple
import sys
from itertools import combinations

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _get_column_as_string(m: List[str], col: int) -> str:
    return "".join(row[col] for row in m)


def _expand_universe(m: List[str]) -> Tuple[List[str], List[Tuple[int, int]]]:
    """
    Espande l'universo raddoppiando righe e colonne che non contengono galassie.
    Ritorna la nuova mappa e le coordinate delle galassie.
    """
    # Righe
    rows = m[:]
    for i in range(len(rows) - 1, -1, -1):
        if "#" not in rows[i]:
            rows.insert(i, "." * len(rows[i]))

    # Colonne
    for j in range(len(rows[0]) - 1, -1, -1):
        col_str = _get_column_as_string(rows, j)
        if "#" not in col_str:
            rows = [row[:j] + "." + row[j:] for row in rows]

    galaxies: List[Tuple[int, int]] = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                galaxies.append((r, c))
    return rows, galaxies


def _write_universe(m: List[str], file_name: str = "universe.txt") -> None:
    out_path = Path(__file__).with_name(file_name)
    with out_path.open("w", encoding="utf8") as f:
        for row in m:
            f.write(row + "\n")


def _get_empty_rows_cols(m: List[str]) -> Tuple[List[int], List[int]]:
    empty_rows: List[int] = []
    empty_cols: List[int] = []

    for r, row in enumerate(m):
        if "#" not in row:
            empty_rows.append(r)

    for c in range(len(m[0])):
        col_str = _get_column_as_string(m, c)
        if "#" not in col_str:
            empty_cols.append(c)

    return empty_rows, empty_cols


def _get_galaxies(m: List[str]) -> List[Tuple[int, int]]:
    galaxies: List[Tuple[int, int]] = []
    for r, row in enumerate(m):
        for c, ch in enumerate(row):
            if ch == "#":
                galaxies.append((r, c))
    return galaxies


def _distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _expanded_distance(a: Tuple[int, int], b: Tuple[int, int],
                       empty_rows: List[int], empty_cols: List[int],
                       expansion_factor: int) -> int:
    """
    Distanza manhattan tra a e b considerando che le righe/colonne vuote
    valgono 'expansion_factor' invece di 1.
    """
    base = _distance(a, b)
    r1, r2 = sorted((a[0], b[0]))
    c1, c2 = sorted((a[1], b[1]))

    extra_rows = sum(1 for r in empty_rows if r1 < r < r2)
    extra_cols = sum(1 for c in empty_cols if c1 < c < c2)

    # Ogni riga/colonna vuota aggiunge (expansion_factor - 1) alla distanza
    return base + (extra_rows + extra_cols) * (expansion_factor - 1)


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = [line for line in raw.splitlines() if line]

    # Per la parte 1 possiamo usare l'espansione esplicita (come nella soluzione originale)
    expanded, galaxies = _expand_universe(grid)
    _write_universe(expanded, "universe.txt")

    total = 0
    for g1, g2 in combinations(galaxies, 2):
        total += _distance(g1, g2)
    return total


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = [line for line in raw.splitlines() if line]

    expansion_factor = 1_000_000
    galaxies = _get_galaxies(grid)
    empty_rows, empty_cols = _get_empty_rows_cols(grid)

    total = 0
    for g1, g2 in combinations(galaxies, 2):
        total += _expanded_distance(g1, g2, empty_rows, empty_cols, expansion_factor)
    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
