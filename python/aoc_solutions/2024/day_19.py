from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_input(raw: str) -> Tuple[List[str], List[str]]:
    """
    Input del tipo:

        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        ...

    Torna:
      - lista di towels
      - lista di pattern
    """
    lines = [ln.strip() for ln in raw.splitlines()]
    # prima riga: elenco di towels, separati da comma+spazio
    towels = [t.strip() for t in lines[0].split(",")]

    # dopo una riga vuota arrivano i patterns
    patterns = [ln for ln in lines[2:] if ln]

    return towels, patterns


# ---------------------------------------------------------------------------
# Core: conteggio dei modi & feasibility
# ---------------------------------------------------------------------------

def count_patterns(raw: str) -> Tuple[int, int]:
    """
    Restituisce (part1, part2):

    - part1: quanti pattern sono *possibili* (almeno 1 modo di comporli)
    - part2: per tutti i pattern, la somma di QUANTI modi esistono
    """
    towels, patterns = parse_input(raw)

    @lru_cache(maxsize=None)
    def count_ways(s: str) -> int:
        """
        Ritorna il numero di modi per comporre la stringa s usando i towels.
        """
        if not s:
            return 1
        ways = 0
        for towel in towels:
            if s.startswith(towel):
                ways += count_ways(s[len(towel):])
        return ways

    part1 = 0
    part2 = 0

    for pattern in patterns:
        ways = count_ways(pattern)
        if ways > 0:
            part1 += 1
        part2 += ways

    return part1, part2


# ---------------------------------------------------------------------------
# Solve 1 & 2
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    part1, _ = count_patterns(raw)
    return part1


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    _, part2 = count_patterns(raw)
    return part2


if __name__ == "__main__":
    test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    print(f"Part 1 (test): {solve_1(test)}")
    print(f"Part 2 (test): {solve_2(test)}")

    print(f"Part 1 (input reale): {solve_1()}")
    print(f"Part 2 (input reale): {solve_2()}")
