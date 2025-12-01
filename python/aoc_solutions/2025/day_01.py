from __future__ import annotations

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

    operations = inputs_1.splitlines()
    start = 50
    result = 0
    print(start)
    for operation in operations:
        direction, value = operation[0], int(operation[1:])
        if direction == "L" : value *= -1
        start = (start + value) % 100
        if start == 0: result += 1
    
    return result


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    operations = [
        [
            int(line[0].replace("R", "1").replace("L", "-1")),
            int(line[1:])
         ] 
        for line in inputs_1.splitlines()]
    
    result = 0
    start = 50
    for step, lenght in operations:
        for _ in range(lenght):
            start = (start + step) % 100
            if start == 0:
                result += 1            

    return result


if __name__ == "__main__":
    test = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
