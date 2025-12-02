from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

CURRENT_YEAR = 2015

GI = GetInput()

CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


def _find_min_house_part1(target: int) -> int:
    """
    Ogni elfo e porta 10 * e regali a TUTTI i multipli di e.
    Cerchiamo la casa con numero minimo che raggiunge almeno `target` regali.
    """
    # Partiamo da una stima, se non basta raddoppiamo il limite e riproviamo.
    max_house = max(1, target // 10)

    while True:
        presents = [0] * (max_house + 1)

        for elf in range(1, max_house + 1):
            gift = 10 * elf
            for house in range(elf, max_house + 1, elf):
                presents[house] += gift

        for house in range(1, max_house + 1):
            if presents[house] >= target:
                return house

        # Nessuna casa ha raggiunto il target, allarghiamo la ricerca
        max_house *= 2


def _find_min_house_part2(target: int) -> int:
    """
    Parte 2:
    - Ogni elfo e porta 11 * e regali
    - Solo alle prime 50 case multiple di e.
    """
    max_house = max(1, target // 11)

    while True:
        presents = [0] * (max_house + 1)

        for elf in range(1, max_house + 1):
            gift = 11 * elf
            last_house = min(max_house, elf * 50)
            for house in range(elf, last_house + 1, elf):
                presents[house] += gift

        for house in range(1, max_house + 1):
            if presents[house] >= target:
                return house

        max_house *= 2


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    target = int(raw.strip())
    return _find_min_house_part1(target)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    target = int(raw.strip())
    return _find_min_house_part2(target)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
