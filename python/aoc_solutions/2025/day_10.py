from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias

from itertools import combinations
from functools import reduce
import operator

GI = GetInput()

Light: TypeAlias = int
Button: TypeAlias = int
Machine: TypeAlias = tuple[Light,list[Button]]

def xor_all(buttons: list[Button]) -> int:
    return reduce(operator.xor, buttons, 0)


def unique_combs(buttons: list[Button]) -> list[list[Button]]:
    n = len(buttons)
    out: list[list[Button]] = list()
    for r in range(1, n + 1):
        for combo in combinations(buttons, r):
            out.append(list(combo))
    return out


def solve_machine(machine: Machine, toggle: bool = True) -> int:
    possible_results: list[list[Button]] = list()
    target: Light = machine[0]
    buttons: list[Button] = machine[1]
    
    for comb in unique_combs(buttons):
        if xor_all(comb) == target:
            possible_results.append(comb)

    possible_results.sort(key=lambda x: len(x))

    return len(possible_results[0])

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res : int = 0
    machines : list[Machine]  = list()
    for line in inputs_1.strip().splitlines():
        pieces = line.split(' ')
        tmp_light_strm2: str = pieces[0].strip('[]').replace('.', '0').replace('#', '1')
        tmp_light: Light = int(tmp_light_strm2,2)

        len_light : int = len(str(tmp_light_strm2))
        
        tmp_buttons: list[Button] = list()
        for piece in pieces[1:]:
            if "{" in piece:
                continue
            tmp_button: list[str] = ['0'] * len_light
            indexes: list[int] = [ int(el) 
                                   for el in piece.strip('()').split(",")
                                 ]
            for i in indexes:
                tmp_button[i] = '1'
            
            button: Button = int(''.join(tmp_button),2)
            tmp_buttons.append(button)
        tmp_machine: Machine = (tmp_light,tmp_buttons)
        machines.append(tmp_machine)

        res += solve_machine(tmp_machine)
    
    return res


def solve_2(test_string: str | None = None) -> int:
    _inputs_1 = GI.input if test_string is None else test_string

    
    return 0


if __name__ == "__main__":
    
    test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
