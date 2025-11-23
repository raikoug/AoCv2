from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


def _is_triangle(a: int, b: int, c: int) -> bool:
    s = sorted((a, b, c))
    return s[0] + s[1] > s[2]


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    possible = 0
    for line in raw.splitlines():
        if not line.strip():
            continue
        sides = [int(num) for num in line.split() if num]
        if len(sides) != 3:
            continue
        if _is_triangle(*sides):
            possible += 1
    return possible


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = [line for line in raw.splitlines() if line.strip()]
    possible = 0

    for i in range(0, len(lines), 3):
        group = lines[i : i + 3]
        if len(group) < 3:
            break
        nums = [row.split() for row in group]
        # colonne verticali
        t1 = [int(nums[0][0]), int(nums[1][0]), int(nums[2][0])]
        t2 = [int(nums[0][1]), int(nums[1][1]), int(nums[2][1])]
        t3 = [int(nums[0][2]), int(nums[1][2]), int(nums[2][2])]

        for t in (t1, t2, t3):
            if _is_triangle(*t):
                possible += 1

    return possible


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
