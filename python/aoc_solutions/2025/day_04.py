from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import Callable, TypeAlias

GI = GetInput()

# D : list[(row,col)]
D = [(-1,-1), (-1,0), (-1,1),
     (0,-1)         , (0,1),
     (1,-1), (1,0), (1,1)]

Point: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[str]

point_sum: Callable[[Point, Point], Point] = lambda x,y : (x[0]+y[0], x[1]+y[1] )
get_grid_p: Callable[[Grid,Point], str] = lambda g,p : g[p[0]][p[1]]
row : Callable[[Point], int] = lambda p: p[0]
col : Callable[[Point], int] = lambda p: p[1]

def str_setitem(s: str, c: str, i: int) -> str:
    if len(c) != 1:
        raise ValueError("c shoudl be char")
    if not 0 <= i < len(s):
        raise IndexError("index out of range")
    return s[:i] + c + s[i+1:]

def check_p(p: Point, r: range, c: range) -> bool:
    return all([ row(p) in r, col(p) in c ])

def get_agj_n(grid: Grid, p: Point) -> int:
    #print(f"Checking {p} - ", end = "")
    row_range:range = range(0,len(grid))
    col_range:range = range(0,len(grid[0]))
    temp = 0
    for new_p in [ point_sum(p,d) for d in D 
                      if check_p(point_sum(p,d),row_range,col_range)
                      ]:
        #print(f"{new_p}:{get_grid_p(grid,new_p)}", end = "")
        if get_grid_p(grid,new_p) == "@": 
            temp += 1 
            #print(f" +1 !!!", end = "")
    #print()
    return temp

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res: int = 0
    grid : Grid = inputs_1.strip().splitlines()
    for row,line in enumerate(grid):
        for col,char in enumerate(line):
            if char == "@" and get_agj_n(grid,(row,col)) < 4:
                res += 1
    return res

def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res: int = 0
    old_res: int = 0
    grid : Grid = inputs_1.strip().splitlines()
    to_remove: list[Point] = list()
    while 1:
        for row,line in enumerate(grid):
            for col,char in enumerate(line):
                if char == "@" and get_agj_n(grid,(row,col)) < 4:
                    res += 1
                    to_remove.append((row,col))
        if res == old_res:
            break
        old_res = res
        while to_remove:
            p = to_remove.pop(0)
            grid[p[0]] = str_setitem(grid[p[0]],".", p[1])

    return res

if __name__ == "__main__":
    test = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
