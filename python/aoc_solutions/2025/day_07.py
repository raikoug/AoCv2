from __future__ import annotations

from pathlib import Path
import sys
from queue import Queue
from typing import TypeAlias, Callable

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput

GI = GetInput()

row: TypeAlias = int
col: TypeAlias = int

Point: TypeAlias = tuple[row,col]
Queueelement: TypeAlias = Point
QueueelementV2: TypeAlias = tuple[int,Point]
Grid: TypeAlias = list[str]
Direction: TypeAlias = tuple[row,col]

MAX_ROW: int = 0
MAX_COL: int = 0


def get_grid(g: Grid, p: Point, d: Direction) -> list[tuple[Point, str]]:
    global MAX_ROW, MAX_COL

    new_row: row = p[0] + d[0]
    new_col: col = p[1] + d[1]

    # fuori dai bordi? nessuna cella valida
    if not (0 <= new_row <= MAX_ROW):
        return []
    if not (0 <= new_col <= MAX_COL):
        return []
    
    return [((new_row, new_col), g[new_row][new_col])]

def get_split(g: Grid, p: Point) -> list[tuple[Point, str]]:
    res = list()
    for d in [(0,1), (0,-1)]:
        new_row: row = p[0] + d[0]
        new_col: col = p[1] + d[1]

        # fuori dai bordi? nessuna cella valida
        if not (0 <= new_row <= MAX_ROW) or not (0 <= new_col <= MAX_COL):
            continue
        
        res.append(((new_row, new_col), g[new_row][new_col]))
    
    return res


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    global MAX_ROW
    global MAX_COL

    grid: Grid = inputs_1.strip('\n').splitlines()
    row,col = 0,0
    found = False
    start: Point = (0,0)
    for row,line in enumerate(grid):
        for col, char in enumerate(line):
            if char.lower() == 's':
                start = (row,col)
                found = True
                break
        if found:
            break
    
    MAX_ROW = len(grid) - 1
    MAX_COL = len(grid[0]) - 1

    splitter_seen: set[Point] = set()
    position_seen: set[Point] = set()
    first_queue_element: Queueelement = (start)
    q: Queue[Queueelement]= Queue()
    q.put(first_queue_element)

    while not q.empty():
        beam: Point = q.get()
        
        actual_pos = (beam[0]+1,beam[1])

        res = get_grid(grid,actual_pos,(1,0))
        if not res:
            continue
        else:
            next_pos, char = res[0]
        
        if next_pos in position_seen:
            continue
            
        if char == ".":
            q.put(next_pos)
            position_seen.add(next_pos)
        else:
            splitter_seen.add(next_pos)

            actual_pos = next_pos
            
            for dir in [(0,1), (0,-1)]:
                res = get_grid(grid,actual_pos,dir)
                if not res:
                    continue

                next_pos, char = res[0]
                if next_pos in position_seen:
                    continue

                q.put(next_pos)
                position_seen.add(next_pos)


    return len(splitter_seen)


from functools import lru_cache


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    grid: Grid = inputs_1.strip('\n').splitlines()
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    # trova la S
    start: Point | None = None
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            if ch.lower() == 's':
                start = (r, c)
                break
        if start is not None:
            break

    if start is None:
        raise ValueError("No start found")
    
    @lru_cache(maxsize=None)
    def timelines_from(r: int, c: int) -> int:
        ch = grid[r][c]

        if ch == '.' or ch == 'S':
            nr = r + 1
            if nr > max_row:
                return 1
            return timelines_from(nr, c)

        elif ch == '^':
            total = 0
            # ramo sinistro e destro
            for dc in (-1, 1):
                nc = c + dc
                if 0 <= nc <= max_col:
                    total += timelines_from(r, nc)
                else:
                    total += 1
            return total

        else:
            raise ValueError(f"Unexpected char: {ch!r}, in {(r, c)}")

    # risultato: timeline da S
    return timelines_from(*start)



if __name__ == "__main__":
    test = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
