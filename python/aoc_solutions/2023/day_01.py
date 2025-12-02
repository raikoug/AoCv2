from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


_DIGIT_WORDS: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def _extract_digits_part2(line: str) -> list[int]:
    """Estrae i 'digit' da una riga considerando sia cifre sia parole (one, two, ...)."""
    digits: list[int] = []
    n = len(line)

    for i in range(n):
        ch = line[i]
        if ch.isdigit():
            digits.append(int(ch))
            continue

        # controllo parole numeriche
        for word, value in _DIGIT_WORDS.items():
            if line.startswith(word, i):
                digits.append(value)
                break

    return digits


def solve_1(test_string: Optional[str] = None) -> int:
    """
    Part 1: per ogni riga prende il primo e l'ultimo carattere numerico,
    li combina in un numero a due cifre e somma tutti questi valori.
    """
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        digits = [ch for ch in line if ch.isdigit()]
        if not digits:
            # nel puzzle reale non succede, ma teniamoci safe
            continue

        value = int(digits[0] + digits[-1])
        total += value

    return total


def solve_2(test_string: Optional[str] = None) -> int:
    """
    Part 2: come la parte 1, ma i digit possono essere anche parole
    ('one', 'two', ...). Le parole possono sovrapporsi (es. 'oneight').
    """
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        digits = _extract_digits_part2(line)
        if not digits:
            continue

        value = digits[0] * 10 + digits[-1]
        total += value

    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
