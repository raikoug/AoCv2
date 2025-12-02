from __future__ import annotations

from pathlib import Path
from typing import Literal, Set
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

# === Type alias ===
Direction = Literal["^", ">", "v", "<"]
Pos = tuple[int, int]
Grid = list[list[str]]
Visited = Set[Pos]
State = tuple[int, int, Direction]

# Direzioni: N, E, S, W
DIRECTIONS: list[Direction] = ["^", ">", "v", "<"]

M: dict[Direction, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}

D: dict[Direction, Direction] = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}


def _parse_grid(raw: str) -> tuple[Grid, Pos]:
    """Parsa la stringa di input in una griglia e trova la posizione iniziale '^'."""
    grid: Grid = [list(line) for line in raw.splitlines()]
    start: Pos | None = None

    for i, row in enumerate(grid):
        try:
            guard_col = row.index("^")
        except ValueError:
            continue

        start = (i, guard_col)
        # Sostituisci il simbolo del guardiano con un punto
        grid[i][guard_col] = "."
        break

    if start is None:
        raise ValueError("Guardiano non trovato nella mappa.")

    return grid, start


def _simulate(grid: Grid, start: Pos) -> tuple[Grid, Visited, Pos]:
    """
    Simula il percorso del guardiano:

    - Ritorna la griglia (modificata solo togliendo '^'),
      l'insieme delle posizioni visitate,
      e la posizione di start.
    - Se viene rilevato un loop, l'insieme visited è vuoto (sentinel).
    """
    current_row, current_col = start
    current_dir: Direction = "^"

    visited_tiles: Visited = {start}
    seen_states: Set[State] = {(current_row, current_col, current_dir)}

    rows, cols = len(grid), len(grid[0])

    while True:
        # Calcola la nuova posizione basata sulla direzione attuale
        delta_row, delta_col = M[current_dir]
        new_row = current_row + delta_row
        new_col = current_col + delta_col

        # Verifica se il guardiano esce dalla mappa
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            break  # Fine del percorso

        # Controlla se c'è un ostacolo
        if grid[new_row][new_col] == "#":
            # Gira a destra
            current_dir = D[current_dir]
            continue

        # Muovi il guardiano avanti
        current_row, current_col = new_row, new_col

        # Controlla se lo stato corrente è già stato visto
        current_state: State = (current_row, current_col, current_dir)
        if current_state in seen_states:
            # Loop rilevato: usiamo visited vuoto come segnale
            return grid, set(), start

        seen_states.add(current_state)
        visited_tiles.add((current_row, current_col))

    return grid, visited_tiles, start


def solve_1(
    test_string: str | None = None,
    grid: Grid | None = None,
    start: Pos | None = None,
) -> tuple[Grid, Visited, Pos]:
    """
    - Se `grid` è None, prende l'input da GI (o da `test_string`) e parsa tutto.
    - Altrimenti usa `grid` e `start` forniti.
    - Ritorna (grid, visited, start).
    """
    if grid is None:
        inputs_1 = GI.input if test_string is None else test_string
        if inputs_1 is None:
            raise ValueError("Nessun input fornito.")
        grid, start_pos = _parse_grid(inputs_1)
    else:
        if start is None:
            raise ValueError("Quando passi una grid devi passare anche start.")
        start_pos = start

    return _simulate(grid, start_pos)


def solve_2(grid: Grid, visited: Visited, start: Pos) -> int:
    """
    Prova a mettere un ostacolo '#' in ogni casella visitata (tranne lo start)
    e conta quante volte si genera un loop.
    """
    # Non consideriamo la casella di partenza tra quelle in cui mettere '#'
    visited_without_start: Visited = set(visited)
    visited_without_start.discard(start)

    loops = 0
    max_visited = len(visited_without_start)

    for i, point in enumerate(visited_without_start):
        print(f"Evaluating position {i + 1: >3} of {max_visited}", end="")
        grid[point[0]][point[1]] = "#"

        # Rilancia la simulazione con la stessa griglia e lo stesso start
        _, result, _ = solve_1(grid=grid, start=start)
        if not result:
            loops += 1

        # rollback
        print(f" Done! Loop count: {loops}", end="\r")
        grid[point[0]][point[1]] = "."

    print()
    return loops


if __name__ == "__main__":
    test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    # Usa input reale da GetInput:
    grid, visited, start = solve_1()
    # Oppure per test:
    # grid, visited, start = solve_1(test_string=test)

    if visited:
        print(f"Part 1: {len(visited)}")
        print(f"Part 2: {solve_2(grid, visited, start)}")
    else:
        print("Loop rilevato! Nessuna posizione unica restituita.")
