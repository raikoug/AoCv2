from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Coord = Tuple[int, int]


def parse(src: str) -> List[str]:
    """Ritorna la lista dei codici (una riga per codice), ignorando righe vuote."""
    return [line.strip() for line in src.splitlines() if line.strip()]


def distance(start: Coord, end: Coord) -> Coord:
    """Ritorna il vettore (dx, dy) tra due coordinate."""
    return end[0] - start[0], end[1] - start[1]


numeric_coord: Dict[str, Coord] = {
    "A": (2, 3),
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
}

coord_numeric: Dict[Coord, str] = {v: k for k, v in numeric_coord.items()}

direction_coord: Dict[str, Coord] = {
    "A": (2, 0),
    "^": (1, 0),
    ">": (2, 1),
    "v": (1, 1),
    "<": (0, 1),
}

coord_direction: Dict[Coord, str] = {v: k for k, v in direction_coord.items()}


@lru_cache(maxsize=None)
def move(button: str, next_button: str, numeric: bool) -> str:
    """
    Restituisce la sequenza di tasti (sul keypad corrente) per muovere il cursore
    da `button` a `next_button`, terminando con 'A'.

    `numeric` indica se stiamo usando il keypad numerico (True) o quello direzionale (False).
    """
    if button == next_button:
        return "A"

    if numeric:
        button_coord = numeric_coord
        coord_button = coord_numeric
    else:
        button_coord = direction_coord
        coord_button = coord_direction

    first_coord = button_coord[button]
    next_coord = button_coord[next_button]
    dx, dy = distance(first_coord, next_coord)

    # movimenti in x
    move_x = ">" * dx if dx >= 0 else "<" * (-dx)
    # movimenti in y
    move_y = "v" * dy if dy >= 0 else "^" * (-dy)

    # se ci si muove solo in una direzione, niente ambiguità
    if dx == 0:
        return move_y + "A"
    if dy == 0:
        return move_x + "A"

    # altrimenti, bisogna stare attenti ai "buchi" della tastiera
    candidates: List[str] = []

    # prima muovo in x, poi in y
    if (next_coord[0], first_coord[1]) in coord_button:
        candidates.append(move_x + move_y + "A")

    # prima muovo in y, poi in x
    if (first_coord[0], next_coord[1]) in coord_button:
        candidates.append(move_y + move_x + "A")

    # se c'è una sola sequenza valida (o dx < 0), prendiamo la prima
    if len(candidates) != 2 or dx < 0:
        return candidates[0]

    # se ci sono due sequenze valide e dx > 0, prendiamo la seconda
    return candidates[1]


@lru_cache(maxsize=None)
def get_sequence_length(sequence: str, indirection: int, numeric: bool) -> int:
    """
    Calcola la lunghezza della sequenza prodotta dopo `indirection` livelli di robot.

    - Se `indirection == 0`, la "lunghezza" è semplicemente len(sequence).
    - Altrimenti:
      - Prependiamo 'A' (posizione iniziale sul keypad).
      - Spezziamo la sequenza in coppie (current, next).
      - Per ogni coppia calcoliamo la sequenza di press sul livello inferiore
        con `move(...)` e richiamiamo ricorsivamente `get_sequence_length` con
        `indirection - 1` e `numeric=False` (controller direzionale).
    """
    if indirection == 0:
        return len(sequence)

    sequence = "A" + sequence
    total = 0

    for b, nb in zip(sequence, sequence[1:]):
        sub_seq = move(b, nb, numeric)
        total += get_sequence_length(sub_seq, indirection - 1, False)

    return total


def solve_1(test_string: str | None = None) -> int:
    data = GI.input if test_string is None else test_string
    codes = parse(data)
    inner_robots = 2  # come nel tuo originale
    # outer robot + inner robots (per la numeric keypad)
    indirection = inner_robots + 1

    total = 0
    for code in codes:
        length = get_sequence_length(code, indirection, True)
        numeric_value = int(code[:-1])  # parte numerica del codice
        total += length * numeric_value

    return total


def solve_2(test_string: str | None = None) -> int:
    data = GI.input if test_string is None else test_string
    codes = parse(data)
    inner_robots = 25
    indirection = inner_robots + 1

    total = 0
    for code in codes:
        length = get_sequence_length(code, indirection, True)
        numeric_value = int(code[:-1])
        total += length * numeric_value

    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
