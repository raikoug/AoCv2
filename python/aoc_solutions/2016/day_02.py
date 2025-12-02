from __future__ import annotations

from pathlib import Path
from typing import Optional, Self

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


class Button:
    val: str
    U: "Button"
    R: "Button"
    D: "Button"
    L: "Button"

    def __init__(self, val: int | str) -> None:
        self.val = str(val)


def _code_part1(raw: str) -> str:
    res = ""

    uno = Button(1)
    due = Button(2)
    tre = Button(3)
    quattro = Button(4)
    cinque = Button(5)
    sei = Button(6)
    sette = Button(7)
    otto = Button(8)
    nove = Button(9)

    uno.U = uno
    uno.R = due
    uno.D = quattro
    uno.L = uno

    due.U = due
    due.R = tre
    due.D = cinque
    due.L = uno

    tre.U = tre
    tre.R = tre
    tre.D = sei
    tre.L = due

    quattro.U = uno
    quattro.R = cinque
    quattro.D = sette
    quattro.L = quattro

    cinque.U = due
    cinque.R = sei
    cinque.D = otto
    cinque.L = quattro

    sei.U = tre
    sei.R = sei
    sei.D = nove
    sei.L = cinque

    sette.U = quattro
    sette.R = otto
    sette.D = sette
    sette.L = sette

    otto.U = cinque
    otto.R = nove
    otto.D = otto
    otto.L = sette

    nove.U = sei
    nove.R = nove
    nove.D = nove
    nove.L = otto

    actual = cinque
    for line in raw.splitlines():
        if not line:
            continue
        for move in line.strip():
            if move == "R":
                actual = actual.R
            elif move == "L":
                actual = actual.L
            elif move == "D":
                actual = actual.D
            elif move == "U":
                actual = actual.U
        res += actual.val

    return res


def _code_part2(raw: str) -> str:
    res = ""

    uno = Button(1)
    due = Button(2)
    tre = Button(3)
    quattro = Button(4)
    cinque = Button(5)
    sei = Button(6)
    sette = Button(7)
    otto = Button(8)
    nove = Button(9)
    A = Button("A")
    B = Button("B")
    C = Button("C")
    D = Button("D")

    uno.U = uno
    uno.R = uno
    uno.D = tre
    uno.L = uno

    due.U = due
    due.R = tre
    due.D = sei
    due.L = due

    tre.U = uno
    tre.R = quattro
    tre.D = sette
    tre.L = due

    quattro.U = quattro
    quattro.R = quattro
    quattro.D = otto
    quattro.L = tre

    cinque.U = cinque
    cinque.R = sei
    cinque.D = cinque
    cinque.L = cinque

    sei.U = due
    sei.R = sette
    sei.D = A
    sei.L = cinque

    sette.U = tre
    sette.R = otto
    sette.D = B
    sette.L = sei

    otto.U = quattro
    otto.R = nove
    otto.D = C
    otto.L = sette

    nove.U = nove
    nove.R = nove
    nove.D = nove
    nove.L = otto

    A.U = sei
    A.R = B
    A.D = A
    A.L = A

    B.U = sette
    B.R = C
    B.D = D
    B.L = A

    C.U = otto
    C.R = C
    C.D = C
    C.L = B

    D.U = B
    D.R = D
    D.D = D
    D.L = D

    actual = cinque
    for line in raw.splitlines():
        if not line:
            continue
        for move in line.strip():
            if move == "R":
                actual = actual.R
            elif move == "L":
                actual = actual.L
            elif move == "D":
                actual = actual.D
            elif move == "U":
                actual = actual.U
        res += actual.val

    return res


def solve_1(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    return _code_part1(inputs_1)


def solve_2(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    return _code_part2(inputs_1)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
