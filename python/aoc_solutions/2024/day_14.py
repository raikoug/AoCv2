from __future__ import annotations

from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import List, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


@dataclass
class Robot:
    row: int       # y
    col: int       # x
    row_speed: int # vy
    col_speed: int # vx


Robots = List[Robot]
Pos = Tuple[int, int]


# --- Parsing --------------------------------------------------------------


def parse_robots(raw: str, is_test: bool) -> tuple[Robots, int, int]:
    """
    Parla le righe tipo:
        p=0,4 v=3,-3
    in una lista di Robot.

    max_row / max_col sono fissate dal puzzle:
    - input reale: 103 x 101
    - input di test: 7 x 11
    """
    max_row = 7 if is_test else 103
    max_col = 11 if is_test else 101

    robots: Robots = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        position, speed = line.split()

        # p=x,y
        position = position.removeprefix("p=")
        col_str, row_str = position.split(",")
        col = int(col_str)
        row = int(row_str)

        # v=dx,dy
        speed = speed.removeprefix("v=")
        col_speed_str, row_speed_str = speed.split(",")
        col_speed = int(col_speed_str)
        row_speed = int(row_speed_str)

        robots.append(
            Robot(
                row=row,
                col=col,
                row_speed=row_speed,
                col_speed=col_speed,
            )
        )

    return robots, max_row, max_col


# --- Simulazione ----------------------------------------------------------


def tick_robots(robots: Robots, steps: int, max_row: int, max_col: int) -> None:
    """
    Aggiorna in-place la posizione di tutti i robot di `steps` secondi,
    con wrapping modulo max_row / max_col.
    """
    for r in robots:
        r.row = (r.row + r.row_speed * steps) % max_row
        r.col = (r.col + r.col_speed * steps) % max_col


def positions_at(robots: Robots, t: int, max_row: int, max_col: int) -> List[Pos]:
    """
    Restituisce la lista di posizioni (row, col) di tutti i robot al tempo t,
    calcolata a partire dallo stato iniziale (senza mutare robots).
    """
    return [
        (
            (r.row + r.row_speed * t) % max_row,
            (r.col + r.col_speed * t) % max_col,
        )
        for r in robots
    ]


# --- Parte 1: fattore di sicurezza per i quadranti ------------------------


def safety_factor(robots: Robots, max_row: int, max_col: int) -> int:
    """
    Calcola il prodotto dei robot nei 4 quadranti, ignorando
    le righe/colonne centrali.
    """
    half_row = max_row // 2
    half_col = max_col // 2

    q1 = q2 = q3 = q4 = 0

    for r in robots:
        # robots sulla riga/colonna centrale -> ignorati
        if r.row == half_row or r.col == half_col:
            continue
        if r.row < half_row and r.col < half_col:
            q1 += 1
        elif r.row < half_row and r.col > half_col:
            q2 += 1
        elif r.row > half_row and r.col < half_col:
            q3 += 1
        elif r.row > half_row and r.col > half_col:
            q4 += 1

    return q1 * q2 * q3 * q4


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    is_test = test_string is not None

    robots, max_row, max_col = parse_robots(inputs_1, is_test=is_test)

    # Dopo 100 secondi:
    tick_robots(robots, 100, max_row, max_col)
    return safety_factor(robots, max_row, max_col)


# --- Parte 2: quando appare l'albero (pattern più "compatto") -------------


def bounding_box_area(positions: List[Pos]) -> int:
    rows = [r for r, _ in positions]
    cols = [c for _, c in positions]
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return width * height


def solve_2(test_string: str | None = None) -> int:
    """
    Strategia classica AoC per questo giorno:

    - Lo stato dei robot è periodico sulla griglia toroidale.
      Un periodo massimo è max_row * max_col (upper bound).
    - Calcoliamo, per ogni t in [0, max_row * max_col), l'area del bounding box
      delle posizioni.
    - Il tempo in cui l'area è minima è quello in cui i robot sono più "compatti"
      e formano il messaggio (l'albero di Natale).

    Restituiamo quel t.
    """
    inputs_1 = GI.input if test_string is None else test_string
    is_test = test_string is not None

    robots, max_row, max_col = parse_robots(inputs_1, is_test=is_test)

    max_steps = max_row * max_col  # bound sul periodo
    best_t = 0
    best_area = float("inf")

    for t in range(max_steps):
        positions = positions_at(robots, t, max_row, max_col)
        area = bounding_box_area(positions)
        if area < best_area:
            best_area = area
            best_t = t

    return best_t


if __name__ == "__main__":
    test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

    print(f"Part 1 (real): {solve_1()}")
    print(f"Part 2 (real): {solve_2()}")
    # Per test:
    # print(f"Part 1 (test): {solve_1(test)}")
    # print(f"Part 2 (test): {solve_2(test)}")
