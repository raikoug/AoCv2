from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

CURRENT_YEAR = 2015

GI = GetInput()


class _LegacyAOC:
    """Compat adapter for old 'aoc.get_input(CURRENT_DAY, part)' API."""

    def get_input(self, *_: int) -> str:
        return GI.input


aoc = _LegacyAOC()

from pathlib import Path
from math import prod
from itertools import combinations

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    packages = [int(pack) for pack in inputs_1.splitlines()]
    target = sum(packages) // 3
    
    result = {"entanglement" : prod(packages), "packages" : len(packages)}
    lenght = 2
    found = False
    while True:
        i = 0
        print(f"Evaluating all the combination of lenght {lenght} with sum {target}")
        for composition in combinations(packages, lenght):
            if sum(composition) == target:
                found = True
                curr_ent = prod(composition)
                if curr_ent < result["entanglement"]:
                    result["entanglement"] = curr_ent
                    result["packages"] = sum(composition)
            i+=1
            #print(f"Evaluated: {i: >5} combinations", end = "\r")
        if found: break
        lenght += 1

    print()
    return result["entanglement"]
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    packages = [int(pack) for pack in inputs_1.splitlines()]
    target = sum(packages) // 4
    
    result = {"entanglement" : prod(packages), "packages" : len(packages)}
    lenght = 2
    found = False
    while True:
        i = 0
        print(f"Evaluating all the combination of lenght {lenght} with sum {target}")
        for composition in combinations(packages, lenght):
            if sum(composition) == target:
                found = True
                curr_ent = prod(composition)
                if curr_ent < result["entanglement"]:
                    result["entanglement"] = curr_ent
                    result["packages"] = sum(composition)
            i+=1
            #print(f"Evaluated: {i: >5} combinations", end = "\r")
        if found: break
        lenght += 1

    print()
    return result["entanglement"]

if __name__ == "__main__":
    test_1 = """1
2
3
4
5
7
8
9
10
11
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
