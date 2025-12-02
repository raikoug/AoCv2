from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Deque, Optional, Set, Tuple
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Pos = Tuple[int, int]


def _is_wall(x: int, y: int, magic: int) -> bool:
    """Ritorna True se la cella (x, y) è un muro."""
    if x < 0 or y < 0:
        return True
    v = x * x + 3 * x + 2 * x * y + y + y * y + magic
    return bin(v).count("1") % 2 == 1


def _neighbors(pos: Pos, magic: int) -> list[Pos]:
    x, y = pos
    res: list[Pos] = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if nx >= 0 and ny >= 0 and not _is_wall(nx, ny, magic):
            res.append((nx, ny))
    return res


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    magic = int(raw.strip())
    start: Pos = (1, 1)
    target: Pos = (31, 39)

    queue: Deque[Tuple[Pos, int]] = deque([(start, 0)])
    visited: Set[Pos] = {start}

    while queue:
        pos, dist = queue.popleft()
        if pos == target:
            return dist

        for nb in _neighbors(pos, magic):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, dist + 1))

    raise RuntimeError("Percorso non trovato")


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    magic = int(raw.strip())
    start: Pos = (1, 1)

    queue: Deque[Tuple[Pos, int]] = deque([(start, 0)])
    visited: Set[Pos] = {start}

    while queue:
        pos, dist = queue.popleft()
        if dist == 50:
            continue
        for nb in _neighbors(pos, magic):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, dist + 1))

    return len(visited)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
