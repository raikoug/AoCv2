from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Grid = List[List[str]]
Pos = Tuple[int, int]

MOVES: dict[str, Pos] = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


# ---------------------------------------------------------------------------
# Parsing input
# ---------------------------------------------------------------------------

def parse_input(raw: str) -> tuple[Grid, str]:
    """
    Divide l'input in:
    - griglia del magazzino
    - stringa di mosse (tutte le righe concatenate)
    """
    maze_raw, moves_raw = raw.strip().split("\n\n", 1)
    grid: Grid = [list(line) for line in maze_raw.splitlines()]
    moves = "".join(moves_raw.splitlines())
    return grid, moves


def find_robot(grid: Grid) -> Pos:
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "@":
                return r, c
    raise ValueError("Robot '@' non trovato nella griglia.")


# ---------------------------------------------------------------------------
# Parte 1
# ---------------------------------------------------------------------------

def step_part1(grid: Grid, robot: Pos, move: str) -> Pos:
    dr, dc = MOVES[move]
    r, c = robot
    nr, nc = r + dr, c + dc
    target = grid[nr][nc]

    if target == "#":
        # muro: non ci muoviamo
        return robot

    if target == ".":
        # cella vuota: sposta solo il robot
        grid[nr][nc] = "@"
        grid[r][c] = "."
        return nr, nc

    if target == "O":
        # stiamo cercando di spingere una fila di box
        cr, cc = nr, nc
        while grid[cr][cc] == "O":
            cr += dr
            cc += dc

        if grid[cr][cc] != ".":
            # c'è un muro o qualcosa di solido: non possiamo spingere
            return robot

        # c'è spazio: mettiamo una box in fondo e spostiamo il robot
        grid[cr][cc] = "O"
        grid[nr][nc] = "@"
        grid[r][c] = "."
        return nr, nc

    # qualunque altro simbolo: non previsto in part1
    return robot


def gps_sum_part1(grid: Grid) -> int:
    total = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "O":
                total += r * 100 + c
    return total


def solve_1(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    grid, moves = parse_input(inputs_1)

    robot = find_robot(grid)
    for m in moves:
        robot = step_part1(grid, robot, m)

    return gps_sum_part1(grid)


# ---------------------------------------------------------------------------
# Parte 2: griglia "wide" con box larghi '[ ]'
# ---------------------------------------------------------------------------

def widen_grid(grid: Grid) -> Grid:
    """
    Converte la griglia part1 in quella part2:
    - '#' -> '##'
    - '.' -> '..'
    - 'O' -> '[]'
    - '@' -> '@.'
    """
    new_grid: Grid = []
    for row in grid:
        new_row: list[str] = []
        for ch in row:
            if ch == "#":
                new_row.extend(["#", "#"])
            elif ch == ".":
                new_row.extend([".", "."])
            elif ch == "O":
                new_row.extend(["[", "]"])
            elif ch == "@":
                new_row.extend(["@", "."])
            else:
                raise ValueError(f"Carattere inatteso in griglia: {ch}")
        new_grid.append(new_row)
    return new_grid


def gps_sum_part2(grid: Grid) -> int:
    """
    Ora i box sono '[ ]'. Il GPS si calcola usando solo la cella
    sinistra ('[') come posizione del box.
    """
    total = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "[":
                total += r * 100 + c
    return total


# --- Movimento orizzontale (part2) ----------------------------------------

def step_part2_horizontal(grid: Grid, robot: Pos, dr: int, dc: int) -> Pos:
    r, c = robot
    nr, nc = r + dr, c + dc
    target = grid[nr][nc]

    if target == "#":
        return robot

    if target == ".":
        grid[nr][nc] = "@"
        grid[r][c] = "."
        return nr, nc

    if target not in "[]":
        # Non dovrebbe succedere, ma nel dubbio non ci muoviamo
        return robot

    # Stiamo spingendo un blocco orizzontale di box larghi
    rows = len(grid)
    cols = len(grid[0])

    # Trova tutti i box (cella sinistra '[') lungo la direzione orizzontale
    boxes: set[Pos] = set()
    cr, cc = nr, nc
    while 0 <= cr < rows and 0 <= cc < cols:
        ch = grid[cr][cc]
        if ch not in "[]":
            break

        if ch == "[":
            left_col = cc
        else:  # ']'
            left_col = cc - 1

        boxes.add((cr, left_col))
        cc += dc

    # La cella dopo l'ultimo box deve essere vuota per poter spingere
    if not (0 <= cr < rows and 0 <= cc < cols):
        return robot
    if grid[cr][cc] != ".":
        return robot

    # Possiamo spostare: muoviamo i box dal più lontano al più vicino
    # verso la direzione del movimento
    reverse = (dc == 1)  # se andiamo a destra, partiamo da quelli più a destra
    for br, bc in sorted(boxes, key=lambda p: p[1], reverse=reverse):
        # Cancella posizione corrente
        grid[br][bc] = "."
        grid[br][bc + 1] = "."
        # Nuova posizione
        nb_c = bc + dc
        grid[br][nb_c] = "["
        grid[br][nb_c + 1] = "]"

    # Sposta il robot
    grid[r][c] = "."
    grid[nr][nc] = "@"
    return nr, nc


# --- Movimento verticale (part2) ------------------------------------------

def collect_boxes_vertical(grid: Grid, robot: Pos, dr: int) -> tuple[bool, set[Pos]]:
    """
    Determina se è possibile spingere i box verticalmente (su/giù) di una cella.

    Ritorna (ok, boxes):
    - ok: True se si può spingere (nessun muro incontrato),
    - boxes: insieme delle celle sinistre ('[') di tutti i box da muovere.
    """
    rows = len(grid)
    cols = len(grid[0])
    r, c = robot

    to_visit: list[Pos] = [(r + dr, c)]
    visited: set[Pos] = set()
    boxes: set[Pos] = set()

    while to_visit:
        rr, cc = to_visit.pop()
        if not (0 <= rr < rows and 0 <= cc < cols):
            # Fuori griglia => in AoC è circondato da muri, ma meglio essere safe
            return False, set()

        if (rr, cc) in visited:
            continue
        visited.add((rr, cc))

        ch = grid[rr][cc]

        if ch == "#":
            return False, set()
        if ch == ".":
            continue

        if ch == "[":
            left_col = cc
        elif ch == "]":
            left_col = cc - 1
        else:
            # Qualunque altra cosa (per es. '@') non dovrebbe capitare nella catena
            continue

        # Aggiungi questo box
        boxes.add((rr, left_col))

        # Controlla le celle sopra/sotto entrambe le metà del box
        for col in (left_col, left_col + 1):
            nr = rr + dr
            if 0 <= nr < rows:
                to_visit.append((nr, col))

    return True, boxes


def step_part2_vertical(grid: Grid, robot: Pos, dr: int) -> Pos:
    ok, boxes = collect_boxes_vertical(grid, robot, dr)
    if not ok:
        return robot

    r, c = robot

    # Svuota tutte le posizioni attuali dei box
    for br, bc in boxes:
        grid[br][bc] = "."
        grid[br][bc + 1] = "."

    # Scrivi le nuove posizioni
    for br, bc in boxes:
        nr = br + dr
        grid[nr][bc] = "["
        grid[nr][bc + 1] = "]"

    # Sposta il robot
    nr = r + dr
    grid[r][c] = "."
    grid[nr][c] = "@"
    return nr, c


def step_part2(grid: Grid, robot: Pos, move: str) -> Pos:
    dr, dc = MOVES[move]
    if dr != 0:  # movimento verticale
        return step_part2_vertical(grid, robot, dr)
    else:        # movimento orizzontale
        return step_part2_horizontal(grid, robot, dr, dc)


def solve_2(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    grid1, moves = parse_input(inputs_1)

    # Converte griglia alla versione "wide"
    grid = widen_grid(grid1)
    robot = find_robot(grid)

    for m in moves:
        robot = step_part2(grid, robot, m)

    return gps_sum_part2(grid)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test manuali puoi fare qualcosa tipo:
    #
    # test_input = """#######
    # #...#.#
    # #.....#
    # #..OO@#
    # #..O..#
    # #.....#
    # #######
    #
    # <vv<<^^<<^^
    # """
    # print("Test P1:", solve_1(test_input))
    # print("Test P2:", solve_2(test_input))
