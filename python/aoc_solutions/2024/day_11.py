from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import Iterable, List

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Stone = int
StonesLine = List[Stone]

PART_1_BLINKS = 25
PART_2_BLINKS = 75


# --- Helpers --------------------------------------------------------------


def stone_has_even_digits(stone: Stone) -> bool:
    """Ritorna True se il numero di cifre della pietra è pari."""
    return len(str(stone)) % 2 == 0


@cache
def split_string_by_half(stone: Stone) -> tuple[Stone, Stone]:
    """
    Divide la rappresentazione decimale di stone in due metà
    e ritorna le due parti come interi.
    Esempio: 1234 -> (12, 34)
    """
    s = str(stone)
    h = len(s) // 2
    return int(s[:h]), int(s[h:])


@cache
def count_after_blinks(stone: Stone, blinks: int) -> int:
    """
    Restituisce quante pietre risultano da UNA pietra iniziale `stone`
    dopo `blinks` lampeggi, applicando le regole del puzzle.

    Usiamo cache per (stone, blinks) così il costo esplosivo viene
    “schiacciato” dal memoization.
    """
    if blinks == 0:
        # Nessun blink: la pietra esiste ancora come singola
        return 1

    # Un blink: applica la regola e somma le pietre risultanti
    if stone == 0:
        # 0 -> 1
        return count_after_blinks(1, blinks - 1)

    if stone_has_even_digits(stone):
        # split in due metà
        left, right = split_string_by_half(stone)
        return (
            count_after_blinks(left, blinks - 1)
            + count_after_blinks(right, blinks - 1)
        )

    # altrimenti: stone -> stone * 2024
    return count_after_blinks(stone * 2024, blinks - 1)


def total_stones_after_blinks(stones: Iterable[Stone], blinks: int) -> int:
    """
    Dato un elenco di pietre iniziali e un numero di blinks,
    restituisce il totale delle pietre risultanti.
    """
    return sum(count_after_blinks(stone, blinks) for stone in stones)


def parse_stones_line(raw: str) -> StonesLine:
    return [int(el) for el in raw.split() if el]


# --- Soluzioni richieste dal template -------------------------------------


def solve_1(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    stones = parse_stones_line(inputs_1)
    return total_stones_after_blinks(stones, PART_1_BLINKS)


def solve_2(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    stones = parse_stones_line(inputs_1)
    return total_stones_after_blinks(stones, PART_2_BLINKS)


if __name__ == "__main__":
    test = "0 1 10 99 999"
    test_2 = "125 17"

    # Input reale da AOC
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test veloci:
    # print(f"Part 1 (test): {solve_1(test)}")
    # print(f"Part 2 (test): {solve_2(test_2)}")
