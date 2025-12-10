from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias

GI = GetInput()

Light: TypeAlias = str
Button: TypeAlias = str
Machine: TypeAlias = tuple[Light,list[Button]]

def solve_machine(machine: Machine, toggle: bool = True) -> int:
    res = 1

    target: Light = machine[0]
    buttons: list[Button] = machine[1]


    return res

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    machines : list[Machine]  = list()
    for line in inputs_1.strip().splitlines():
        pieces = line.split(' ')
        tmp_ligt: Light = pieces[0].strip('[]').replace('.', '0').replace('#', '1')
        len_light : int = len(tmp_ligt)
        
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
            
            button: Button = ''.join(tmp_button)
            tmp_buttons.append(button)
        tmp_machine: Machine = (tmp_ligt,tmp_buttons)
        machines.append(tmp_machine)
        print(f"{line} -> {tmp_machine}")
        
    
    
    return 0


def solve_2(test_string: str | None = None) -> int:
    _inputs_1 = GI.input if test_string is None else test_string

    
    return 0


if __name__ == "__main__":
    
    test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    print(f"Part 1: {solve_1(test)}")
    print(f"Part 2: {solve_2()}")
