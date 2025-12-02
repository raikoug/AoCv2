from __future__ import annotations

from hashlib import md5
from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _find_lowest_number(salt: str, prefix: str) -> int:
    """Trova il più piccolo intero n tale che
    md5(f"{salt}{n}") inizi con `prefix`.
    """
    n = 0
    while True:
        digest = md5(f"{salt}{n}".encode("utf-8")).hexdigest()
        if digest.startswith(prefix):
            return n
        n += 1


def solve_1(test_string: Optional[str] = None) -> int:
    """Part 1 – md5(salt + n) che inizia con 5 zeri esadecimali."""
    salt = (GI.input if test_string is None else test_string).strip()
    return _find_lowest_number(salt, "00000")


def solve_2(test_string: Optional[str] = None) -> int:
    """Part 2 – md5(salt + n) che inizia con 6 zeri esadecimali."""
    salt = (GI.input if test_string is None else test_string).strip()
    return _find_lowest_number(salt, "000000")


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
