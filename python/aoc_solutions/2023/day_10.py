from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Tuple
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

# Mappa dei pezzi di tubo: per ogni simbolo, gli spostamenti possibili (row_delta, col_delta)
PM = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


@dataclass
class Worm:
    row: int
    col: int
    start_row: int
    start_col: int
    prev_row: int
    prev_col: int
    symbol: str
    path: List[Tuple[int, int]]
    path_set: Set[Tuple[int, int]]

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.start_row = row
        self.start_col = col
        self.prev_row = row
        self.prev_col = col
        self.symbol = "S"
        self.path = [(row, col)]
        self.path_set = {(row, col)}

    def move_to(self, row: int, col: int, grid: List[str]) -> None:
        self.prev_row, self.prev_col = self.row, self.col
        self.row, self.col = row, col
        self.symbol = grid[row][col]
        coord = (row, col)
        self.path.append(coord)
        self.path_set.add(coord)


def _trace_loop(grid: List[str]) -> Worm:
    """Segue il loop a partire da 'S' e restituisce il worm con il percorso completo."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    start_row = -1
    start_col = -1
    for i, line in enumerate(grid):
        j = line.find("S")
        if j != -1:
            start_row, start_col = i, j
            break
    if start_row == -1:
        raise ValueError("Nessun punto di partenza 'S' trovato nella mappa.")

    worm = Worm(start_row, start_col)

    # Prima mossa: cerca un vicino che si colleghi a S
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    moved = False
    for dr, dc in directions:
        nr, nc = start_row + dr, start_col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            ch = grid[nr][nc]
            if ch in PM and (-dr, -dc) in PM[ch]:
                worm.move_to(nr, nc, grid)
                moved = True
                break
    if not moved:
        raise ValueError("Impossibile trovare un primo passo valido dal punto 'S'.")

    # Seguiamo il loop finché non torniamo a S
    while not (worm.row == worm.start_row and worm.col == worm.start_col):
        ch = worm.symbol
        if ch == "S":
            break
        if ch not in PM:
            raise ValueError(f"Simbolo di tubo inatteso: {ch!r} in ({worm.row},{worm.col})")
        for dr, dc in PM[ch]:
            nr, nc = worm.row + dr, worm.col + dc
            if (nr, nc) == (worm.prev_row, worm.prev_col):
                continue
            if 0 <= nr < rows and 0 <= nc < cols:
                worm.move_to(nr, nc, grid)
                break
        else:
            # Nessuna mossa valida trovata
            break

    return worm


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = [line for line in raw.splitlines() if line]
    worm = _trace_loop(grid)
    # Il percorso include S all'inizio e anche alla fine,
    # quindi la lunghezza effettiva del loop è len(path) - 1
    loop_len = max(0, len(worm.path) - 1)
    return loop_len // 2


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = [line for line in raw.splitlines() if line]
    worm = _trace_loop(grid)

    total_inside_tiles = 0
    out_path = Path(__file__).with_name("TF")

    with out_path.open("w", encoding="utf8") as f:
        for i, row in enumerate(grid):
            we_are_inside = False
            rendered_row: List[str] = []
            for j, ch in enumerate(row):
                coord = (i, j)
                if coord in worm.path_set:
                    # Disegniamo il tubo e aggiorniamo lo stato "dentro/fuori"
                    if ch == "J":
                        rendered_row.append("┘")
                        we_are_inside = not we_are_inside
                    elif ch == "L":
                        rendered_row.append("└")
                        we_are_inside = not we_are_inside
                    elif ch == "7":
                        rendered_row.append("┐")
                    elif ch == "F":
                        rendered_row.append("┌")
                    elif ch == "|":
                        rendered_row.append("│")
                        we_are_inside = not we_are_inside
                    elif ch == "-":
                        rendered_row.append("─")
                    elif ch == "S":
                        rendered_row.append("S")
                else:
                    if we_are_inside:
                        total_inside_tiles += 1
                        rendered_row.append("█")
                    else:
                        rendered_row.append(" ")
            f.write("".join(rendered_row) + "\n")

    return total_inside_tiles


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
