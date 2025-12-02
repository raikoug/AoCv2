from __future__ import annotations

from hashlib import md5
from pathlib import Path
from queue import PriorityQueue
from typing import List, Tuple
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

D = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}

OPEN_CHARS = "bcdef"


def _md5_hex(s: str) -> str:
    return md5(s.encode()).hexdigest()


def move(pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    dx, dy = D[direction]
    return pos[0] + dx, pos[1] + dy


def find_open_doors(md5sum: str) -> List[str]:
    res: List[str] = []
    if md5sum[0] in OPEN_CHARS:
        res.append("U")
    if md5sum[1] in OPEN_CHARS:
        res.append("D")
    if md5sum[2] in OPEN_CHARS:
        res.append("L")
    if md5sum[3] in OPEN_CHARS:
        res.append("R")
    return res


def around_me(code: str, x: int, y: int) -> List[str]:
    res: List[str] = []
    open_doors = find_open_doors(_md5_hex(code))
    # UP
    if y > 0 and "U" in open_doors:
        res.append("U")
    # RIGHT
    if x < 3 and "R" in open_doors:
        res.append("R")
    # DOWN
    if y < 3 and "D" in open_doors:
        res.append("D")
    # LEFT
    if x > 0 and "L" in open_doors:
        res.append("L")
    return res


def solve_1(test_string: str | None = None) -> str:
    raw = GI.input if test_string is None else test_string
    passcode = raw.strip()

    q: PriorityQueue[Tuple[int, Tuple[int, int], str]] = PriorityQueue()
    q.put((0, (0, 0), ""))

    while not q.empty():
        steps, pos, path = q.get()
        x, y = pos
        for direction in around_me(f"{passcode}{path}", x, y):
            new_pos = move(pos, direction)
            new_path = path + direction
            if new_pos == (3, 3):
                return new_path
            q.put((steps + 1, new_pos, new_path))

    raise RuntimeError("Nessun percorso trovato")


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    passcode = raw.strip()

    q: PriorityQueue[Tuple[int, Tuple[int, int], str]] = PriorityQueue()
    q.put((0, (0, 0), ""))
    max_steps = 0

    while not q.empty():
        steps, pos, path = q.get()
        x, y = pos
        for direction in around_me(f"{passcode}{path}", x, y):
            new_pos = move(pos, direction)
            new_path = path + direction
            if new_pos == (3, 3):
                if steps + 1 > max_steps:
                    max_steps = steps + 1
            else:
                q.put((steps + 1, new_pos, new_path))

    return max_steps


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
