from __future__ import annotations
from re import findall
import re

from pathlib import Path
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    regex = r'mul\((\d{1,3}),(\d{1,3})\)'
    finds = findall(regex,inputs_1)
    total = 0
    for find in finds:
        total += int(find[0])*int(find[1])
    return total


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    mul_regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    do_regex = re.compile(r'do\(\)')
    dont_regex = re.compile(r'don\'t\(\)')

    total_sum = 0
    mul_enabled = True  

    index = 0
    length = len(inputs_1)
    
    while index < length:
        do_match = do_regex.match(inputs_1, index)
        dont_match = dont_regex.match(inputs_1, index)
        mul_match = mul_regex.match(inputs_1, index)    
        if do_match:
            mul_enabled = True
            index += do_match.end() - do_match.start()
        elif dont_match:
            mul_enabled = False
            index += dont_match.end() - dont_match.start()
        elif mul_match and mul_enabled:
            x, y = mul_match.groups()
            total_sum += int(x) * int(y)
            index += mul_match.end() - mul_match.start()
        else:
            index += 1
    return total_sum


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
