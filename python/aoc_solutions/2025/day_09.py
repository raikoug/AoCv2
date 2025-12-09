from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias, Callable


GI = GetInput()

corner : TypeAlias = tuple[int,int]

Area : Callable[[corner,corner], int] = lambda a,b : abs(a[0]-b[0]) * abs(a[1]-b[1])



def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    corners : list[tuple[int,int]] = list()
    for line in inputs_1.strip().splitlines():
        x,y = line.split(",")
        corner = (int(x), int(y))
        
        corners.append(corner)

    
    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
