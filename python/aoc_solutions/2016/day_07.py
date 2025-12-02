from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys
from re import findall

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))

regex_abba = r"(\w)(\w)\2\1"
regex_aba = r"(?=((\w)(\w))\2)"


def _split_good_bad(line: str) -> tuple[list[str], list[str]]:
    good: list[str] = []
    bad: list[str] = []
    tmp = ""
    parsing_g = True
    for char in line:
        div = "[" if parsing_g else "]"
        if char == div:
            if parsing_g:
                good.append(tmp)
            else:
                bad.append(tmp)
            parsing_g = not parsing_g
            tmp = ""
        else:
            tmp += char

    if parsing_g:
        good.append(tmp)
    else:
        bad.append(tmp)
    return good, bad


def abba_in_str(piece: str) -> bool:
    for el in findall(regex_abba, piece):
        if el[0] != el[1]:
            return True
    return False


def check(line: str) -> bool:
    good, bad = _split_good_bad(line)

    can_go = any(abba_in_str(piece) for piece in good)
    if not can_go:
        return False

    # nessun ABBA nei blocchi tra []
    return not any(abba_in_str(piece) for piece in bad)


def aba_in_str(piece: str) -> list[list[str]]:
    coppie: list[list[str]] = []
    for el in findall(regex_aba, piece):
        if el[1] != el[2]:
            tmp_coppia = [el[1], el[2]]
            if tmp_coppia not in coppie:
                coppie.append(tmp_coppia)
    return coppie


def coppia_in_str(coppie: list[list[str]], piece: str) -> bool:
    for coppia in coppie:
        ricerca = f"{coppia[1]}{coppia[0]}{coppia[1]}"
        if ricerca in piece:
            return True
    return False


def check2(line: str) -> bool:
    good, bad = _split_good_bad(line)

    coppie: list[list[str]] = []
    for piece in good:
        tmp_coppie = aba_in_str(piece)
        for coppia in tmp_coppie:
            if coppia not in coppie:
                coppie.append(coppia)

    if not coppie:
        return False

    for piece in bad:
        if coppia_in_str(coppie, piece):
            return True

    return False


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    count = 0
    for line in inputs_1.splitlines():
        line = line.strip()
        if line and check(line):
            count += 1
    return count


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    count = 0
    for line in inputs_1.splitlines():
        line = line.strip()
        if line and check2(line):
            count += 1
    return count


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
