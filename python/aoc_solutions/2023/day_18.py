from __future__ import annotations

from pathlib import Path
from typing import Optional, Iterable, Tuple, List
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


Coord = tuple[int, int]


def _parse_lines(raw: str) -> list[tuple[str, int, str]]:
    res: list[tuple[str, int, str]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        d, n, color = line.split()
        res.append((d, int(n), color.strip("()")))
    return res


def _compute_lagoon_area(moves: Iterable[tuple[int, int]]) -> int:
    # moves: (dx, dy) in sequenza, partendo da (0,0)
    x, y = 0, 0
    vertices: list[Coord] = [(x, y)]
    perimeter = 0
    for dx, dy in moves:
        x += dx
        y += dy
        vertices.append((x, y))
        perimeter += abs(dx) + abs(dy)

    # Shoelace formula (area firmata *2)
    area2 = 0
    for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1]):
        area2 += x1 * y2 - x2 * y1
    area = abs(area2) // 2

    # Pick: A = I + B/2 - 1  => I = A - B/2 + 1
    # Celle totali = I + B
    boundary = perimeter
    interior = area - boundary // 2 + 1
    return interior + boundary


def _moves_part1(spec: list[tuple[str, int, str]]) -> list[tuple[int, int]]:
    dirs: dict[str, Coord] = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }
    moves: list[tuple[int, int]] = []
    for d, n, _ in spec:
        dx, dy = dirs[d]
        moves.append((dx * n, dy * n))
    return moves


def _moves_part2(spec: list[tuple[str, int, str]]) -> list[tuple[int, int]]:
    # colore tipo '#70c710'
    # primi 5 hex = passi, ultima cifra = direzione 0..3
    dir_map: dict[str, Coord] = {
        "0": (1, 0),   # R
        "1": (0, 1),   # D
        "2": (-1, 0),  # L
        "3": (0, -1),  # U
    }
    moves: list[tuple[int, int]] = []
    for _, __, color in spec:
        assert color.startswith("#")
        code = color[1:]
        steps_hex = code[:5]
        dir_digit = code[5]
        steps = int(steps_hex, 16)
        dx, dy = dir_map[dir_digit]
        moves.append((dx * steps, dy * steps))
    return moves


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    spec = _parse_lines(raw)
    moves = _moves_part1(spec)
    return _compute_lagoon_area(moves)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    spec = _parse_lines(raw)
    moves = _moves_part2(spec)
    return _compute_lagoon_area(moves)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
