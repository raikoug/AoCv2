from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def solve_1(test_string: Optional[str] = None) -> int:
    """
    Part 1 – Calcola il piano finale:
    '(' = +1, ')' = -1
    """
    s = GI.input if test_string is None else test_string
    return s.count("(") - s.count(")")


def solve_2(test_string: Optional[str] = None) -> int:
    """
    Part 2 – Trova il primo indice (1-based) in cui il piano diventa -1.
    """
    s = GI.input if test_string is None else test_string

    floor = 0
    for idx, ch in enumerate(s, start=1):
        floor += 1 if ch == "(" else -1
        if floor == -1:
            return idx

    # Se non scende mai al piano -1, restituiamo -1 (o potremmo sollevare un errore)
    return -1


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
