from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    s = inputs_1.strip()
    i = 0
    new_line = ""

    while i < len(s):
        if s[i] == "(":
            i += 1
            chars = ""
            times = ""
            flag = False
            while s[i] != ")":
                if s[i].isdigit() and not flag:
                    chars += s[i]
                elif s[i].isdigit() and flag:
                    times += s[i]
                elif s[i] == "x":
                    flag = True
                i += 1
            # s[i] = ")"
            chars_int = int(chars)
            times_int = int(times)
            new_line += s[i + 1 : i + 1 + chars_int] * times_int
            i = i + chars_int + 1
        else:
            new_line += s[i]
            i += 1

    return len(new_line)


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    s = inputs_1.strip()

    total = 0
    v = [1] * len(s)
    i = 0

    while i < len(s):
        if s[i] != "(":
            total += v[i]
            i += 1
            continue

        # s[i] == "("
        i += 1
        start = i
        while s[i] != ")":
            i += 1
        pattern = s[start:i]
        length_str, times_str = pattern.split("x")
        length = int(length_str)
        times = int(times_str)
        i += 1  # posizioniamo su primo carattere da moltiplicare

        for j in range(i, i + length):
            v[j] *= times

    return total


if __name__ == "__main__":
    # test = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
