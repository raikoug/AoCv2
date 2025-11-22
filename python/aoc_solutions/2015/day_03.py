from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Set, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Pos = Tuple[int, int]

V: Dict[str, Pos] = {
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
}


def vector_sum(a: Pos, b: Pos) -> Pos:
    return a[0] + b[0], a[1] + b[1]


def walk(
    moves: str,
    start: Pos = (0, 0),
    visited: Optional[Set[Pos]] = None,
) -> Set[Pos]:
    """
    Esegue la sequenza di mosse partendo da `start` e aggiorna l'insieme `visited`.

    Ritorna l'insieme di tutte le posizioni visitate.
    """
    if visited is None:
        visited = {start}
    pos = start
    for ch in moves:
        dv = V.get(ch)
        if dv is None:
            # Ignoriamo caratteri non validi
            continue
        pos = vector_sum(pos, dv)
        visited.add(pos)
    return visited


def solve_1(test_string: Optional[str] = None) -> int:
    """
    Part 1 – Numero di case che ricevono almeno un regalo da Babbo Natale.
    """
    s = GI.input if test_string is None else test_string
    visited = walk(s)
    return len(visited)


def solve_2(test_string: Optional[str] = None) -> int:
    """
    Part 2 – Numero di case che ricevono almeno un regalo da Babbo Natale + Robo-Santa.
    Si alternano i passi:
      - Santa: mosse in posizione pari (0,2,4,...)
      - Robo-Santa: mosse in posizione dispari (1,3,5,...)
    """
    s = GI.input if test_string is None else test_string

    santa_moves = s[0::2]
    robo_moves = s[1::2]

    visited: Set[Pos] = {(0, 0)}
    walk(santa_moves, start=(0, 0), visited=visited)
    walk(robo_moves, start=(0, 0), visited=visited)

    return len(visited)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
