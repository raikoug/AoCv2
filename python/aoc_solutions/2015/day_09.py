from __future__ import annotations

from itertools import permutations
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

DistanceMap = Dict[Tuple[str, str], int]


def _parse_distances(raw: str) -> Tuple[DistanceMap, Set[str]]:
    distances: DistanceMap = {}
    places: Set[str] = set()

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        city1, _, city2, _, dist_str = line.split()
        dist = int(dist_str)
        places.add(city1)
        places.add(city2)
        distances[(city1, city2)] = dist
        distances[(city2, city1)] = dist

    return distances, places


def _route_distance(route: Tuple[str, ...], dist: DistanceMap) -> int:
    return sum(dist[(route[i], route[i + 1])] for i in range(len(route) - 1))


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    distances, places = _parse_distances(raw)

    best = float("inf")
    for route in permutations(places, len(places)):
        d = _route_distance(route, distances)
        if d < best:
            best = d

    return int(best)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    distances, places = _parse_distances(raw)

    worst = 0
    for route in permutations(places, len(places)):
        d = _route_distance(route, distances)
        if d > worst:
            worst = d

    return int(worst)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
