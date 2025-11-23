from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    # TODO: implementare la logica della parte 1 (assembunny / esecuzione istruzioni)
    # Usa `raw.splitlines()` per ottenere le istruzioni.
    return 0


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    # TODO: implementare la logica della parte 2
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
