from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

import re


GI = GetInput()

OFFSET_PART2 = 10_000_000_000_000


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass(frozen=True)
class Machine:
    a: Pos  # Button A vector
    b: Pos  # Button B vector
    prize: Pos


BUTTON_A_RE = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
BUTTON_B_RE = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
PRIZE_RE = re.compile(r"Prize: X=(\d+), Y=(\d+)")


def parse_machines(raw: str) -> List[Machine]:
    """
    Parla l'input in blocchi del tipo:

        Button A: X+..., Y+...
        Button B: X+..., Y+...
        Prize: X=..., Y=...

    (eventuale riga vuota tra un blocco e l'altro viene ignorata).
    """
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    machines: List[Machine] = []

    if len(lines) % 3 != 0:
        raise ValueError("Input non in blocchi da 3 righe (A, B, Prize).")

    for i in range(0, len(lines), 3):
        a_line = lines[i]
        b_line = lines[i + 1]
        p_line = lines[i + 2]

        ma = BUTTON_A_RE.match(a_line)
        mb = BUTTON_B_RE.match(b_line)
        mp = PRIZE_RE.match(p_line)

        if not (ma and mb and mp):
            raise ValueError(f"Righe non nel formato atteso vicino a:\n{a_line}\n{b_line}\n{p_line}")

        ax, ay = (int(z) for z in ma.groups())
        bx, by = (int(z) for z in mb.groups())
        px, py = (int(z) for z in mp.groups())

        machines.append(
            Machine(
                a=Pos(ax, ay),
                b=Pos(bx, by),
                prize=Pos(px, py),
            )
        )

    return machines


def min_tokens(a: Pos, b: Pos, prize: Pos) -> Optional[int]:
    """
    Risolve:

        a.x * l + b.x * m = prize.x
        a.y * l + b.y * m = prize.y

    con l, m >= 0 interi.
    Restituisce 3*l + m se esiste soluzione intera non negativa, altrimenti None.
    """
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    px, py = prize.x, prize.y

    det = ax * by - ay * bx
    if det == 0:
        # Vettori paralleli / degeneri: per l'input AOC reale non dovrebbero comparire.
        return None

    # Formula di Cramer
    l_num = px * by - py * bx
    m_num = ax * py - ay * px

    if l_num % det != 0 or m_num % det != 0:
        return None

    l = l_num // det
    m = m_num // det

    if l < 0 or m < 0:
        return None

    return 3 * l + m


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    machines = parse_machines(inputs_1)

    total_tokens = 0
    for machine in machines:
        tokens = min_tokens(machine.a, machine.b, machine.prize)
        if tokens is not None:
            total_tokens += tokens

    return total_tokens


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    machines = parse_machines(inputs_1)

    total_tokens = 0
    for machine in machines:
        prize2 = Pos(
            machine.prize.x + OFFSET_PART2,
            machine.prize.y + OFFSET_PART2,
        )
        tokens = min_tokens(machine.a, machine.b, prize2)
        if tokens is not None:
            total_tokens += tokens

    return total_tokens


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
