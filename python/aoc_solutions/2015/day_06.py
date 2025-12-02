from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Tuple

import sys

import numpy as np

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Command = Tuple[str, int, int, int, int]  # (op, x1, y1, x2, y2)


def _parse_commands(raw: str) -> Iterable[Command]:
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("turn on"):
            op = "on"
            rest = line[len("turn on ") :]
        elif line.startswith("turn off"):
            op = "off"
            rest = line[len("turn off ") :]
        elif line.startswith("toggle"):
            op = "toggle"
            rest = line[len("toggle ") :]
        else:
            raise ValueError(f"Comando sconosciuto: {line!r}")

        coords = rest.replace(" through ", " ")
        c1, c2 = coords.split(" ")
        x1, y1 = (int(v) for v in c1.split(","))
        x2, y2 = (int(v) for v in c2.split(","))

        yield op, x1, y1, x2, y2


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = np.zeros((1000, 1000), dtype=bool)
    for op, x1, y1, x2, y2 in _parse_commands(raw):
        region = grid[x1 : x2 + 1, y1 : y2 + 1]
        if op == "on":
            region[...] = True
        elif op == "off":
            region[...] = False
        elif op == "toggle":
            region[...] = ~region
    return int(grid.sum())


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid = np.zeros((1000, 1000), dtype=int)
    for op, x1, y1, x2, y2 in _parse_commands(raw):
        region = grid[x1 : x2 + 1, y1 : y2 + 1]
        if op == "on":
            region[...] += 1
        elif op == "off":
            region[...] -= 1
            region[region < 0] = 0
        elif op == "toggle":
            region[...] += 2
    return int(grid.sum())


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
