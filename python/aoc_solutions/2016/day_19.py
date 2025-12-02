from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Deque, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    elves = int(raw.strip())

    # Trova la più grande potenza di 2 <= elves
    best_power = 1
    while best_power * 2 <= elves:
        best_power *= 2

    magic_number = elves - best_power
    lucky_elf = 2 * magic_number + 1
    return lucky_elf


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    elves = int(raw.strip())

    # Implementazione classica con due deque (vedi commenti originali)
    left: Deque[int] = deque()
    right: Deque[int] = deque()

    for i in range(1, elves + 1):
        if i < (elves // 2) + 1:
            left.append(i)
        else:
            right.appendleft(i)

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        # rotazione
        right.appendleft(left.popleft())
        left.append(right.pop())

    return left[0] if left else right[0]


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
