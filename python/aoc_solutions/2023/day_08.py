from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple, Optional, List
import sys
from math import lcm

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _parse(raw: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    directions = lines[0]
    mapping: Dict[str, Tuple[str, str]] = {}
    for line in lines[1:]:
        name, rest = line.split(" = ")
        left, right = rest.strip("()").split(", ")
        mapping[name] = (left, right)
    return directions, mapping


def _steps_to_zzz(directions: str, mapping: Dict[str, Tuple[str, str]]) -> int:
    pos = "AAA"
    steps = 0
    idx = 0
    n = len(directions)
    while pos != "ZZZ":
        d = directions[idx]
        idx = (idx + 1) % n
        left, right = mapping[pos]
        pos = left if d == "L" else right
        steps += 1
    return steps


def _steps_to_first_z(start: str, directions: str, mapping: Dict[str, Tuple[str, str]]) -> int:
    pos = start
    steps = 0
    idx = 0
    n = len(directions)
    while not pos.endswith("Z"):
        d = directions[idx]
        idx = (idx + 1) % n
        left, right = mapping[pos]
        pos = left if d == "L" else right
        steps += 1
    return steps


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    directions, mapping = _parse(raw)
    return _steps_to_zzz(directions, mapping)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    directions, mapping = _parse(raw)
    starts: List[str] = [name for name in mapping.keys() if name.endswith("A")]
    cycles = [_steps_to_first_z(s, directions, mapping) for s in starts]
    result = 1
    for c in cycles:
        result = lcm(result, c)
    return result


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
