from __future__ import annotations

from functools import cache
from hashlib import md5
from pathlib import Path
from typing import Optional
import re
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


@cache
def _md5_once(s: str) -> str:
    return md5(s.encode()).hexdigest()


@cache
def _md5_stretched(s: str) -> str:
    for _ in range(2017):
        s = md5(s.encode()).hexdigest()
    return s


def _find_64th_key(salt: str, hasher) -> int:
    triple_re = re.compile(r"(\w)\1\1")
    keys_found = 0
    i = 0

    while True:
        h = hasher(f"{salt}{i}")
        m = triple_re.search(h)
        if m:
            ch = m.group(1)
            pattern = ch * 5
            for j in range(i + 1, i + 1001):
                if pattern in hasher(f"{salt}{j}"):
                    keys_found += 1
                    if keys_found == 64:
                        return i
                    break
        i += 1


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    salt = raw.strip()
    return _find_64th_key(salt, _md5_once)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    salt = raw.strip()
    return _find_64th_key(salt, _md5_stretched)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
