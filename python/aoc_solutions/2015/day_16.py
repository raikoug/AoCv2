from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

# Rende importabile la classe GetInput dal folder python/
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

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))

TP = {
    "children" : 3,
    "cats" : 7,
    "samoyeds" : 2,
    "pomeranians" : 3,
    "akitas" : 0,
    "vizslas" : 0,
    "goldfish" : 5,
    "trees" : 3,
    "cars" : 2,
    "perfumes" : 1
}

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # i know I have a problem with this........
    get_i = lambda s, i : s.replace(":","").replace(",","").replace("Sue ","").split(" ")[i]
    sues = {
        int(get_i(line,0)) : {
            get_i(line, 1) : int(get_i(line, 2)),
            get_i(line, 3) : int(get_i(line, 4)),
            get_i(line, 5) : int(get_i(line, 6)),
            } 
        for line in inputs_1.splitlines()}
    
    for i in range(1,501):
        ok = True
        sue = sues[i]
        suekeys = sue.keys()
        for k,v in TP.items():
            if k in suekeys:
                if v != sue[k]:
                    ok = False
                    break
        if not ok: continue
        result = i
    
    return result

    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # i know I have a problem with this........
    get_i = lambda s, i : s.replace(":","").replace(",","").replace("Sue ","").split(" ")[i]
    sues = {
        int(get_i(line,0)) : {
            get_i(line, 1) : int(get_i(line, 2)),
            get_i(line, 3) : int(get_i(line, 4)),
            get_i(line, 5) : int(get_i(line, 6)),
            } 
        for line in inputs_1.splitlines()}
    
    for i in range(1,501):
        ok = True
        sue = sues[i]
        suekeys = sue.keys()
        for k,v in TP.items():
            if k in suekeys:
                if k in ["cats", "trees"]:
                    if sue[k] <= v:
                        ok = False
                        break
                elif k in ["pomeranians", "goldfish"]:
                    if sue[k] >=v:
                        ok = False
                        break
                elif v != sue[k]:
                    ok = False
                    break
                
        if not ok: continue
        result = i
    
    return result


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
