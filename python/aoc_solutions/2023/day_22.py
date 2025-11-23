from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


@dataclass
class Brick:
    id: int
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int
    supports: Set[int] = field(default_factory=set)
    supported_by: Set[int] = field(default_factory=set)

    def overlaps_xy(self, other: "Brick") -> bool:
        return not (
            self.x2 < other.x1
            or self.x1 > other.x2
            or self.y2 < other.y1
            or self.y1 > other.y2
        )


def _parse_bricks(raw: str) -> List[Brick]:
    bricks: List[Brick] = []
    for i, line in enumerate(raw.splitlines()):
        line = line.strip()
        if not line:
            continue
        left, right = line.split("~")
        x1, y1, z1 = map(int, left.split(","))
        x2, y2, z2 = map(int, right.split(","))

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))

        bricks.append(Brick(i, x1, y1, z1, x2, y2, z2))
    return bricks


def _settle_bricks(bricks: List[Brick]) -> None:
    """
    Simula la caduta dei mattoni: partendo dal più basso,
    ciascun mattone scende finché non tocca terra (z=1) o altri mattoni.
    """
    bricks.sort(key=lambda b: b.z1)

    for i, brick in enumerate(bricks):
        max_supported_z = 0
        for j in range(i):
            below = bricks[j]
            if brick.overlaps_xy(below):
                if below.z2 > max_supported_z:
                    max_supported_z = below.z2

        shift = brick.z1 - (max_supported_z + 1)
        brick.z1 -= shift
        brick.z2 -= shift


def _build_support_graph(bricks: List[Brick]) -> None:
    for b in bricks:
        b.supports.clear()
        b.supported_by.clear()

    # Per ogni mattone, cerchiamo i mattoni esattamente sotto che lo toccano in XY
    for i, b in enumerate(bricks):
        if b.z1 == 1:
            continue
        for j, below in enumerate(bricks):
            if below.z2 == b.z1 - 1 and b.overlaps_xy(below):
                b.supported_by.add(below.id)
                below.supports.add(b.id)


def _count_safe_to_disintegrate(bricks: List[Brick]) -> int:
    """
    Un mattone è "sicuro da disintegrare" se tutti i mattoni che supporta
    hanno almeno un altro supporto oltre a lui.
    """
    safe = 0
    id_map: Dict[int, Brick] = {b.id: b for b in bricks}

    for b in bricks:
        ok = True
        for above_id in b.supports:
            above = id_map[above_id]
            if len(above.supported_by) == 1:
                ok = False
                break
        if ok:
            safe += 1
    return safe


def _chain_reaction_count(bricks: List[Brick], start_id: int) -> int:
    """
    Quanti mattoni cadono se rimuovo `start_id` e lascio propagare la caduta?
    (Escluso il mattone iniziale.)
    """
    fallen: Set[int] = {start_id}
    stack: List[int] = [start_id]
    id_map: Dict[int, Brick] = {b.id: b for b in bricks}

    while stack:
        cur_id = stack.pop()
        cur = id_map[cur_id]
        for above_id in cur.supports:
            if above_id in fallen:
                continue
            above = id_map[above_id]
            # cade solo se TUTTI i suoi supporti sono già caduti
            if all(s in fallen for s in above.supported_by):
                fallen.add(above_id)
                stack.append(above_id)

    # Non contiamo il mattone originario
    return len(fallen) - 1


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    bricks = _parse_bricks(raw)
    _settle_bricks(bricks)
    _build_support_graph(bricks)
    return _count_safe_to_disintegrate(bricks)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    bricks = _parse_bricks(raw)
    _settle_bricks(bricks)
    _build_support_graph(bricks)

    total = 0
    for b in bricks:
        total += _chain_reaction_count(bricks, b.id)
    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
