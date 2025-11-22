from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Optional

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _parse_dimensions(line: str) -> Tuple[int, int, int]:
    """Parsa una riga tipo '2x3x4' in una tupla (l, w, h)."""
    parts = line.strip().split("x")
    if len(parts) != 3:
        raise ValueError(f"Riga non valida per le dimensioni: {line!r}")
    l, w, h = (int(p) for p in parts)
    return l, w, h


def solve_1(test_string: Optional[str] = None) -> int:
    """
    Part 1 – Calcola i piedi quadrati totali di carta da regalo necessari.
    Formula per ogni pacco:
      2*l*w + 2*w*h + 2*h*l + area del lato più piccolo
    """
    raw = GI.input if test_string is None else test_string
    total_sqf = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        l, w, h = _parse_dimensions(line)
        sides = [l * w, w * h, h * l]
        total_sqf += 2 * sum(sides) + min(sides)

    return total_sqf


def solve_2(test_string: Optional[str] = None) -> int:
    """
    Part 2 – Calcola i piedi di nastro necessari.
    Formula per ogni pacco:
      volume (l*w*h) + perimetro del lato più piccolo (2*(a+b))
    """
    raw = GI.input if test_string is None else test_string
    total_ribbon = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        l, w, h = _parse_dimensions(line)
        dims = sorted([l, w, h])  # i due lati più piccoli
        perimeter = 2 * (dims[0] + dims[1])
        volume = l * w * h
        total_ribbon += perimeter + volume

    return total_ribbon


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
