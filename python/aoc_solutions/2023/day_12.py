from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


@cache
def _springs_finder(row: str, nums: Tuple[int, ...]) -> int:
    """
    Conta il numero di modi per riempire `row` (che deve terminare con '.')
    rispettando la sequenza di gruppi di molle `nums`.

    Implementazione basata sul vecchio solver a nonogrammi, memoizzata.
    """
    if not nums:
        # Nessun gruppo da piazzare: valido solo se non restano '#' forzati.
        return 1 if '#' not in row else 0

    next_part = nums[1:]
    # Numero massimo di punti che possiamo mettere prima del primo blocco
    max_offset = len(row) - sum(nums) - len(next_part)
    total = 0

    for offset in range(max_offset):
        # Costruisco il prefisso: offset di '.', poi il blocco di '#', poi un '.'
        prefix = '.' * offset + '#' * nums[0] + '.'

        # Controllo di compatibilità con la maschera ('.','#','?')
        if all(r in (c, '?') for r, c in zip(row, prefix)):
            # Avanza dopo il prefisso
            rest = row[len(prefix) :]
            if next_part:
                total += _springs_finder(rest, next_part)
            else:
                # Ultimo blocco: valido solo se nel resto non compaiono '#'
                if '#' not in rest:
                    total += 1

    return total


def _parse_line(line: str) -> tuple[str, Tuple[int, ...]]:
    pattern_str, nums_str = line.split()
    groups = tuple(int(n) for n in nums_str.split(','))
    return pattern_str, groups


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        pattern, groups = _parse_line(line)
        # Aggiungo il '.' finale come sentinella per la logica di _springs_finder
        total += _springs_finder(pattern + '.', groups)

    return total


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        pattern, groups = _parse_line(line)
        # Ripeti 5 volte separato da '?', come da testo AoC
        expanded_pattern = '?'.join([pattern] * 5) + '.'
        expanded_groups = groups * 5
        total += _springs_finder(expanded_pattern, expanded_groups)

    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
