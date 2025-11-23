from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys
from hashlib import md5

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


class TooHigh(Exception):
    pass


class AlreadyEvaluated(Exception):
    pass


def solve_1(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    seed = inputs_1.strip()
    i = 0
    code = ""

    while True:
        res = md5(f"{seed}{i}".encode()).hexdigest()
        if res.startswith("00000"):
            code += res[5]
            print(f"Trovato! {code}")
            if len(code) == 8:
                return code
        i += 1


def solve_2(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    seed = inputs_1.strip()
    i = 0
    found = 0
    code: list[Optional[str]] = [None] * 8

    while True:
        res = md5(f"{seed}{i}".encode()).hexdigest()
        i += 1

        if not res.startswith("00000"):
            continue

        print(f"Found a good hash: {res}")
        try:
            pos = int(res[5])
            if pos > 7:
                raise TooHigh
            if code[pos] is not None:
                raise AlreadyEvaluated
        except ValueError:
            print(f"    Discarded because char {res[5]} is not int")
        except TooHigh:
            print(f"    Discarded index {res[5]} is too high")
        except AlreadyEvaluated:
            print(f"    Discarded index {pos} is already set: {code[pos]}")
        else:
            code[pos] = res[6]
            found += 1
            print(f"    code is now {code}")
            if found == 8:
                print("        Finished!")
                return "".join(code)


if __name__ == "__main__":
    # print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
