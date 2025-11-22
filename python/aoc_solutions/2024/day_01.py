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

    left_values = list()
    right_values= list()
    for line in inputs_1.splitlines():
        left, right = line.split("   ")
        left_values.append(int(left))
        right_values.append(int(right))
    left_values.sort()
    right_values.sort()
    summ = 0
    for i in range(len(left_values)):
        summ += abs(left_values[i] - right_values[i])
    
    return summ


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    left_values = list()
    right_values= list()
    for line in inputs_1.splitlines():
        left, right = line.split("   ")
        left_values.append(int(left))
        right_values.append(int(right))
    
    summ = 0
    for i in range(len(left_values)):
        summ += left_values[i] * right_values.count(left_values[i])
    
    return summ


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
