from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from dataclasses import dataclass, field

from math import prod
import numpy as np

GI = GetInput()

@dataclass
class Operation():
    numbers: list[int] = field(default_factory=list)
    operation: str = ""


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    operations : dict[int,Operation] = dict()

    for line in inputs_1.strip().splitlines():
        for col,el in enumerate(line.split()):
            if col not in operations:
                operations[col] = Operation()
            
            if el.isdigit():
                operations[col].numbers.append(int(el))
            else:
                operations[col].operation = el
    

    res: int = 0

    for op in operations.values():
        if op.operation == "+":
            res += sum(op.numbers)
        else:
            res += prod(op.numbers)
    
    return res


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    lines = inputs_1.splitlines()
    matrix = [
                list(line)
                for line in lines
             ]

    arr = np.array(matrix)
    rotarr = np.rot90(arr, k=1)

    res: int = 0
    numbers : list[int] = list()
    operation : str = ""

    for line in rotarr:
        strline = "".join(line)
        if not strline.strip():
            continue

        if strline.strip().isdigit():
            numbers.append(int(strline))
        else:
            operation = strline[-1]
            numbers.append(int(strline[0:-1]))

            #print(f"Operazione corrente: {numbers} - {operation}")
            # operazioni
            if operation == "+":
                res += sum(numbers)
            else:
                res += prod(numbers)

            # reset
            numbers.clear()
            operation = ""

    return res


if __name__ == "__main__":
    test = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
