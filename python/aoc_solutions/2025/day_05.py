from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()

def p_in_ranges(p: int, ranges: list[range]) -> int:
    res: int = 0
    for range in ranges:
        if p in range:
            res += 1
    return res

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    ranges: list[range] = list()
    products: list[int] = list()
    space = False
    for line in inputs_1.strip().splitlines():
        if line:
            if not space:
                lower,upper = line.split("-")
                lower = int(lower)
                upper = int(upper)
                ranges.append(range(lower,upper+1))
            else:
                products.append(int(line))
        else:
            space = not space
    
    res: int = 0
    for p in products:
        if p_in_ranges(p,ranges):
            res += 1
    return res

def is_included(r: tuple[int,int], ranges: list[tuple[int,int]]):
    # check if r in included in all reanges

    pass

def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    ranges: list[tuple[int,int]] = list()
    space = False
    for line in inputs_1.strip().splitlines():
        if line:
            if not space:
                lower,upper = line.split("-")
                lower = int(lower)
                upper = int(upper)
                ranges.append((lower,upper))
        else:
            break
    
    ranges.sort(key= lambda p: p[0])
    for r in ranges:
        print(r)
    res = 0    
    last_id = 0
    for lower,upper in ranges:
        if lower <= last_id:
            lower = last_id + 1
        
        res += (upper - lower) + 1
        last_id = upper
      
        
    
    
    return res


if __name__ == "__main__":
    test = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    test2 = """1-100
2-20"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
