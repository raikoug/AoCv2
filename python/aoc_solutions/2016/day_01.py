from __future__ import annotations

from pathlib import Path
from typing import Optional, Self

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


class Pos:
    x: int
    y: int

    def __init__(self, clone: Optional[Self] = None) -> None:
        if clone is not None:
            self.x = clone.x
            self.y = clone.y
        else:
            self.x = 0
            self.y = 0

    def move_x(self, delta: int) -> None:
        self.x += delta

    def move_y(self, delta: int) -> None:
        self.y += delta

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    __repr__ = __str__

    def __format__(self, _: str) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pos):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)


def _update_direction(direction: str, turn: str) -> str:
    # N,E,S,O (O = Ovest) come nell'originale
    if direction == "N":  # NORTH
        return "E" if turn == "R" else "O"
    if direction == "S":  # SOUTH
        return "O" if turn == "R" else "E"
    if direction == "E":  # EAST
        return "S" if turn == "R" else "N"
    if direction == "O":  # OVEST
        return "N" if turn == "R" else "S"
    raise ValueError(f"Direzione sconosciuta: {direction}")


def _parse_moves(raw: str) -> list[str]:
    return [m.strip() for m in raw.split(",") if m.strip()]


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    pos = Pos()
    direction = "N"
    for move in _parse_moves(inputs_1):
        turn = move[0]
        dist = int(move[1:])
        direction = _update_direction(direction, turn)

        if direction == "N":
            pos.move_y(dist)
        elif direction == "E":
            pos.move_x(dist)
        elif direction == "S":
            pos.move_y(-dist)
        elif direction == "O":
            pos.move_x(-dist)

    return abs(pos.x) + abs(pos.y)


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    pos = Pos()
    visited: list[Pos] = [Pos(pos)]
    direction = "N"

    for move in _parse_moves(inputs_1):
        turn = move[0]
        dist = int(move[1:])
        direction = _update_direction(direction, turn)

        step_dx = step_dy = 0
        if direction == "N":
            step_dx, step_dy = 0, 1
        elif direction == "E":
            step_dx, step_dy = 1, 0
        elif direction == "S":
            step_dx, step_dy = 0, -1
        elif direction == "O":
            step_dx, step_dy = -1, 0

        for _ in range(dist):
            pos.move_x(step_dx)
            pos.move_y(step_dy)
            if pos in visited:
                return abs(pos.x) + abs(pos.y)
            visited.append(Pos(pos))

    # Se non troviamo mai una posizione visitata due volte (teoricamente non succede)
    return abs(pos.x) + abs(pos.y)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
