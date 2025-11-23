from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _parse(raw: str) -> List[List[int]]:
    rows: List[List[int]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append([int(x) for x in line.split()])
    return rows


def _extrapolate_forward(nums: List[int]) -> int:
    layers: List[List[int]] = [nums]
    while any(v != 0 for v in layers[-1]):
        prev = layers[-1]
        layers.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    # aggiungiamo 0 in fondo e risaliamo
    layers[-1].append(0)
    for i in range(len(layers) - 2, -1, -1):
        layers[i].append(layers[i][-1] + layers[i + 1][-1])
    return layers[0][-1]


def _extrapolate_backward(nums: List[int]) -> int:
    layers: List[List[int]] = [nums]
    while any(v != 0 for v in layers[-1]):
        prev = layers[-1]
        layers.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    # aggiungiamo 0 all'inizio e risaliamo verso sinistra
    layers[-1].insert(0, 0)
    for i in range(len(layers) - 2, -1, -1):
        new_first = layers[i][0] - layers[i + 1][0]
        layers[i].insert(0, new_first)
    return layers[0][0]


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    rows = _parse(raw)
    return sum(_extrapolate_forward(r) for r in rows)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    rows = _parse(raw)
    return sum(_extrapolate_backward(r) for r in rows)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
