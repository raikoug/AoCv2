from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, List, Tuple, cast

import sys

from sympy import Symbol, nonlinsolve  # type: ignore[import-untyped]

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()


@dataclass(eq=True)
class Vec3:
    x: float
    y: float
    z: float

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError(index)

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vec3":
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    @staticmethod
    def dot2d(lhs: "Vec3", rhs: "Vec3") -> float:
        return lhs.x * rhs.x + lhs.y * rhs.y


Hailstone = Tuple[Vec3, Vec3]


def _parse_input(data: str) -> List[Hailstone]:
    """
    Ogni riga: 'x, y, z @ dx, dy, dz'
    """
    stones: List[Hailstone] = []
    for line in data.splitlines():
        if not line.strip():
            continue
        parts = [int(n.strip()) for part in line.split("@") for n in part.split(",")]
        x0, y0, z0, dx, dy, dz = parts
        stones.append((Vec3(x0, y0, z0), Vec3(dx, dy, dz)))
    return stones


def _det(a: Vec3, b: Vec3) -> float:
    return a.x * b.y - a.y * b.x


def _line_intersection(start0: Vec3, dir0: Vec3, start1: Vec3, dir1: Vec3) -> Vec3 | None:
    """
    Intersezione 2D delle proiezioni sul piano XY di due traiettorie.
    Ritorna None se non si intersecano nel futuro.
    """
    end0 = start0 + dir0
    end1 = start1 + dir1

    xdiff = Vec3(start0.x - end0.x, start1.x - end1.x, 0.0)
    ydiff = Vec3(start0.y - end0.y, start1.y - end1.y, 0.0)

    div = _det(xdiff, ydiff)
    if div == 0:
        return None

    d = Vec3(_det(start0, end0), _det(start1, end1), 0.0)
    x = _det(d, xdiff) / div
    y = _det(d, ydiff) / div
    intersection = Vec3(x, y, 0.0)

    # Deve essere nel futuro per entrambi
    if Vec3.dot2d(intersection - start0, dir0) < 0:
        return None
    if Vec3.dot2d(intersection - start1, dir1) < 0:
        return None

    return intersection


def _solve_part1(data: str, test_mode: bool) -> int:
    hails = _parse_input(data)
    # range diverso per sample vs input reale
    if test_mode:
        area_min, area_max = 7, 27
    else:
        area_min, area_max = 200000000000000, 400000000000000

    total = 0
    for h0, h1 in combinations(hails, 2):
        inter = _line_intersection(*h0, *h1)
        if inter is None:
            continue
        if area_min <= inter.x <= area_max and area_min <= inter.y <= area_max:
            total += 1
    return total


def _solve_part2(data: str) -> int:
    """
    Trova posizione e velocità del sasso che colpisce tutte le pietre.
    Usa sistema non lineare su 3 hailstones con velocità diverse.
    """
    hails = _parse_input(data)

    # prendi 3 hailstones con velocità 3D distinte
    selected: List[Hailstone] = [hails[0]]
    for h in hails:
        if len(selected) >= 3:
            break
        if not any(existing[1] == h[1] for existing in selected):
            selected.append(h)

    if len(selected) < 3:
        raise ValueError("Non sono riuscito a trovare 3 hailstones con velocità diverse.")

    # Variabili simboliche
    sx, sy, sz = Symbol("s_x"), Symbol("s_y"), Symbol("s_z")
    vx, vy, vz = Symbol("vel_x"), Symbol("vel_y"), Symbol("vel_z")
    t0, t1, t2 = Symbol("t0"), Symbol("t1"), Symbol("t2")

    # Usiamo Any per non litigare con i type stub di sympy
    start_pos: List[Any] = [sx, sy, sz]
    start_vel: List[Any] = [vx, vy, vz]
    times: List[Any] = [t0, t1, t2]

    equations: List[Any] = []
    for i, (pos, vel) in enumerate(selected):
        t = times[i]
        # pos + v * t = hail_pos + hail_v * t  (per x, y, z)
        equations.append(start_pos[0] + start_vel[0] * t - (pos.x + vel.x * t))
        equations.append(start_pos[1] + start_vel[1] * t - (pos.y + vel.y * t))
        equations.append(start_pos[2] + start_vel[2] * t - (pos.z + vel.z * t))

    solution_set = nonlinsolve(equations, [*start_pos, *start_vel, *times])

    # Cast esplicito ad Iterable per accontentare Pylance
    first_solution = next(iter(cast(Iterable[Any], solution_set)))
    sx_sol, sy_sol, sz_sol, *_rest = first_solution

    # Cast a int, i risultati dovrebbero essere interi (o razionali)
    return int(sx_sol) + int(sy_sol) + int(sz_sol)


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    test_mode = test_string is not None
    return _solve_part1(inputs_1, test_mode)


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    return _solve_part2(inputs_1)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
