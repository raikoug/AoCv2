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
import itertools

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    containers = [int(line) for line in inputs_1.splitlines()]
    masks = itertools.product([0, 1], repeat=len(containers))
    combinations = 0
    for mask in masks:
        if sum([a * b for a, b in zip(mask, containers)]) == 150:
            combinations += 1
    return combinations
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    containers = [int(line) for line in inputs_1.splitlines()]
    masks = itertools.product([0, 1], repeat=len(containers))
    combinations = 0
    minimum = 10000
    for mask in masks:
        if sum([a * b for a, b in zip(mask, containers)]) == 150:
            conts = sum(mask)
            if conts < minimum:
                combinations = 1
                minimum = conts
            elif conts == minimum:
                    combinations += 1
            
            
    return combinations, minimum
        
    return 1


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
