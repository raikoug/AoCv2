from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias, Optional, Generator

from itertools import combinations, combinations_with_replacement
from functools import reduce
import operator

GI = GetInput()

Light: TypeAlias = int
Button: TypeAlias = int
Jolts: TypeAlias = list[int]
Machine: TypeAlias = tuple[Light,list[Button], Jolts]

Buttonv2: TypeAlias = list[int]
Machinev2: TypeAlias = tuple[Light,list[Buttonv2], Jolts]

def xor_all(buttons: list[Button]) -> int:
    return reduce(operator.xor, buttons, 0)


def super_combs(
    seq: list[Button],
    r_min: int = 1,
    r_max: Optional[int] = None,
    *,
    dedup_input: bool = True
) -> Generator[list[Button]]:
    items = list(dict.fromkeys(seq)) if dedup_input else list(seq)
    r = r_min
    while True:
        if r_max is not None and r > r_max:
            return
        for combo in combinations_with_replacement(items, r):
            yield list(combo)
        r += 1


def unique_combs(buttons: list[Button]) -> list[list[Button]]:
    n = len(buttons)
    out: list[list[Button]] = list()
    for r in range(1, n + 1):
        for combo in combinations(buttons, r):
            out.append(list(combo))
    return out


def solve_machine(machine: Machine) -> int:
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
        tmp_machine: Machine = (tmp_light,tmp_buttons,[0])
        machines.append(tmp_machine)

        res += solve_machine(tmp_machine)
    
    return res


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    res : int = 0
    machines : list[Machinev2]  = list()
    for line in inputs_1.strip().splitlines():
        pieces = line.split(' ')
        tmp_light_strm2: str = pieces[0].strip('[]').replace('.', '0').replace('#', '1')
        tmp_light: Light = int(tmp_light_strm2,2)

        len_light : int = len(str(tmp_light_strm2))
        jolts: Jolts = list()
        tmp_buttons: list[Buttonv2] = list()
        tmp_button: list[int] = list()
        for piece in pieces[1:]:

            if "{" in piece:
                jolts = [int(el) for el in piece.strip("{}").split(",")]
            elif "(" in piece:
                tmp_button = [0] * len_light
                indexes: list[int] = [ int(el) 
                                    for el in piece.strip('()').split(",")
                                    ]
                for i in indexes:
                    tmp_button[i] = 1
            
                tmp_buttons.append(tmp_button)
        tmp_machine: Machinev2 = (tmp_light,tmp_buttons,jolts)
        machines.append(tmp_machine)

        #res += solve_machine(tmp_machine)
        print(tmp_machine)

    
    return res


if __name__ == "__main__":
    
    test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2(test)}")
