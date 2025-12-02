from __future__ import annotations

from pathlib import Path
from typing import Optional
import re
import string
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def alphabetically_increment(source: str) -> str:
    """Incrementa una password alfabetica in base 26 (a-z)."""
    letters = string.ascii_lowercase
    indexes = [letters.index(ch) for ch in source]
    indexes[-1] += 1

    result: list[int] = []
    carry = False

    for value in reversed(indexes):
        if carry:
            value += 1
            carry = False

        if value == len(letters):
            carry = True
            result.insert(0, 0)
        else:
            result.insert(0, value)

    return "".join(letters[i] for i in result)


def is_next_next(a: str, b: str, c: str) -> bool:
    oa, ob, oc = ord(a), ord(b), ord(c)
    return (ob == oa + 1) and (ob == oc - 1)


def has_ladder(s: str) -> bool:
    """True se la stringa contiene una sequenza incrementale di 3 lettere (es. abc)."""
    for i in range(len(s) - 2):
        if is_next_next(s[i], s[i + 1], s[i + 2]):
            return True
    return False


def has_double_double(s: str) -> bool:
    """True se la stringa contiene almeno due *diverse* coppie di lettere ripetute."""
    regex = r"(.)\1"
    repeats = set(re.findall(regex, s))
    return len(repeats) >= 2


def string_is_ok(source: str) -> bool:
    if not has_ladder(source):
        return False
    if not has_double_double(source):
        return False
    if any(c in source for c in "iol"):
        return False
    return True


def solve_1(test_string: Optional[str] = None) -> str:
    """Restituisce la prossima password valida secondo le regole del giorno 11."""
    raw = GI.input if test_string is None else test_string
    password = raw.strip()

    candidate = alphabetically_increment(password)
    while not string_is_ok(candidate):
        candidate = alphabetically_increment(candidate)
    return candidate


def solve_2(test_string: Optional[str] = None) -> str:
    """Restituisce la password valida successiva a quella di part 1."""
    raw = GI.input if test_string is None else test_string
    first = solve_1(raw)
    second = solve_1(first)
    return second


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
