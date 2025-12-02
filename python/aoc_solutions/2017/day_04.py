from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    res: int = 0

    for line in inputs_1.splitlines():
        words = line.split(" ")
        if len(words) == len(set(words)):
            res += 1

    return res    


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    res: int = 0

    for line in inputs_1.splitlines():
        words = ["".join(sorted(word)) for word in line.split(" ")]
        if len(words) == len(set(words)):
            res += 1

    return res  


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
