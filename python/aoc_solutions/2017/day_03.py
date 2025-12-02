from __future__ import annotations

from pathlib import Path
import sys
from dataclasses import dataclass


PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()



def get_coordinate_of(target: int) -> tuple[int, int]:
    turns = [(1,0), (0,1), (-1,0), (0,-1)]
    turn_index = 0
    distance = 1
    value = 1
    actualx, actualy = 0,0
    steps = 0

    while True:
        turn = turns[turn_index]
        nextx, nexty = actualx + turn[0]*distance, actualy + turn[1]*distance
        actualx, actualy = nextx, nexty

        value += distance
        steps += 1

        turn_index += 1
        turn_index = turn_index % 4

        if steps % 2 == 0:
            distance += 1
        
        if value >= target:
            delta = value - target
            result_x, result_y = actualx - turn[0]*delta, actualy - turn[1]*delta
            return result_x, result_y

def try_get_adj(D: dict, x: int, y: int)->int:
    P = [[x-1,y+1] , [x,y+1], [x+1, y+1],
         [x-1, y]  ,          [x+1, y],
         [x-1, y-1], [x, y-1], [x+1, y-1]
         ]
    res = 0
    for p in P:
        try:
            res += D[(p[0],p[1])]
        except:
            pass
    
    return res

def get_first_larger(target: int) -> tuple[int, int, int]:
    turns = [(1,0), (0,1), (-1,0), (0,-1)]
    turn_index = 0
    distance = 1
    value = 1
    actualx, actualy = 0,0
    steps = 0

    D: dict[tuple[int, int], int] = dict()
    D[(0,0)] = 1

    while True:
        turn = turns[turn_index]
        for i in range(distance):
            nextx, nexty = actualx + turn[0], actualy + turn[1]
            actualx, actualy = nextx, nexty

            value = try_get_adj(D, actualx, actualy)
            if value > target:
                return value, actualx, actualy
            
            D[(actualx, actualy)] = value

        steps += 1

        turn_index += 1
        turn_index = turn_index % 4

        if steps % 2 == 0:
            distance += 1


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    coordinates = get_coordinate_of(int(inputs_1))
    print(coordinates)

    return abs(coordinates[1]) + abs(coordinates[0])


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    value, x, y = get_first_larger(int(inputs_1))
    return value


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
