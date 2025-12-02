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

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    instructions = inputs_1.splitlines()
    max_i = len(instructions) - 1
    registers = dict()
    new = 0
    while new <= max_i:
        cursor = instructions[new]
        if cursor.startswith("hlf"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] //= 2
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("tpl"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] *= 3
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("inc"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] += 1
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("jmp"):
            action = cursor.split(" ")[0]
            jump = int(cursor.split(" ")[1])
            new += jump
            #print(f"{action}, new:{new}")

        elif cursor.startswith("jie"):
            action = cursor.split(" ")[0]
            cursor = cursor.replace(",", "")
            jump = int(cursor.split(" ")[2])
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            
            if registers[reg] % 2 == 0:
                new += jump
            else:
                new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("jio"):
            action = cursor.split(" ")[0]
            cursor = cursor.replace(",", "")
            jump = int(cursor.split(" ")[2])
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0

            if registers[reg] == 1:
                new += jump
            else:
                new += 1
            
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")
  
    print(registers)
    return registers["b"]
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    instructions = inputs_1.splitlines()
    max_i = len(instructions) - 1
    registers = dict()
    registers["a"] = 1
    new = 0
    while new <= max_i:
        cursor = instructions[new]
        if cursor.startswith("hlf"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] //= 2
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("tpl"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] *= 3
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("inc"):
            action = cursor.split(" ")[0]
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            registers[reg] += 1
            new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("jmp"):
            action = cursor.split(" ")[0]
            jump = int(cursor.split(" ")[1])
            new += jump
            #print(f"{action}, new:{new}")

        elif cursor.startswith("jie"):
            action = cursor.split(" ")[0]
            cursor = cursor.replace(",", "")
            jump = int(cursor.split(" ")[2])
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0
            
            if registers[reg] % 2 == 0:
                new += jump
            else:
                new += 1
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")

        elif cursor.startswith("jio"):
            action = cursor.split(" ")[0]
            cursor = cursor.replace(",", "")
            jump = int(cursor.split(" ")[2])
            reg = cursor.split(" ")[1]
            if reg not in registers:
                registers[reg] = 0

            if registers[reg] == 1:
                new += jump
            else:
                new += 1
            
            #print(f"{action}, {reg}:{registers[reg]: >3}, new:{new}")
  
    print(registers)
    return registers["b"]


if __name__ == "__main__":
    test_1 = """inc a
jio a, +2
tpl a
inc a
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
