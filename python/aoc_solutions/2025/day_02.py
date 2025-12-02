from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()

def isNotCorrect(numero: int) -> bool:
    strnum = str(numero)
    if len(strnum) %2 == 0:
        half = len(strnum) // 2
        if strnum[0:half] == strnum[half:]:
            return True
    return False

def isNotCorrectV2(numero: int) -> bool:
    strnum = str(numero)
    length = len(strnum)
    for i in range(1,(length // 2)+1):
        if length % i != 0: continue
        
        pattern = strnum[:i]

        if pattern * (length // i) == strnum:
            return True
        
    return False

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    ranges: list[range] = [ range(int(r.split("-")[0]),int(r.split("-")[1])+1)  
                            for r in inputs_1.strip().split(",")  ]
    res = 0
    for r in ranges:
        for i in r:
            if isNotCorrect(i): res += i 
    return res

def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    ranges: list[range] = [ range(int(r.split("-")[0]),int(r.split("-")[1])+1)  
                            for r in inputs_1.strip().split(",")  ]
    res = 0
    for r in ranges:
        for i in r:
            if isNotCorrectV2(i): res += i 
    return res


if __name__ == "__main__":
    test = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
