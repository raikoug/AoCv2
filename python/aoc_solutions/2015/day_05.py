from __future__ import annotations

from pathlib import Path
from typing import Optional

import re
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _is_nice_part1(s: str) -> bool:
    vowels = sum(s.count(v) for v in "aeiou")
    if vowels < 3:
        return False
    if not any(s[i] == s[i + 1] for i in range(len(s) - 1)):
        return False
    if any(bad in s for bad in ("ab", "cd", "pq", "xy")):
        return False
    return True


def _is_nice_part2(s: str) -> bool:
    # Coppia di due lettere che appare almeno due volte NON sovrapposta
    if not re.search(r"(..).*\1", s):
        return False

    # Una lettera che si ripete con esattamente una in mezzo (xyx)
    if not re.search(r"(.).\1", s):
        return False

    return True



def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    return sum(1 for line in raw.splitlines() if line and _is_nice_part1(line.strip()))


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    return sum(1 for line in raw.splitlines() if line and _is_nice_part2(line.strip()))


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
