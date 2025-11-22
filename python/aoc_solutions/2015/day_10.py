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


def look_and_say(s: str) -> str:
    if not s:
        return ""

    result_parts = []
    current_char = s[0]
    count = 1

    for ch in s[1:]:
        if ch == current_char:
            count += 1
        else:
            result_parts.append(f"{count}{current_char}")
            current_char = ch
            count = 1

    result_parts.append(f"{count}{current_char}")
    return "".join(result_parts)


def _iterate_look_and_say(start: str, times: int) -> str:
    value = start
    for _ in range(times):
        value = look_and_say(value)
    return value


def solve_1(test_string: Optional[str] = None) -> int:
    start = (GI.input if test_string is None else test_string).strip()
    result = _iterate_look_and_say(start, 40)
    return len(result)


def solve_2(test_string: Optional[str] = None) -> int:
    start = (GI.input if test_string is None else test_string).strip()
    result = _iterate_look_and_say(start, 50)
    return len(result)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
