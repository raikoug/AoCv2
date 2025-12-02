from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional, Dict, List
from math import prod

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


MAX_CUBES: Dict[str, int] = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def _parse_game_line(line: str) -> tuple[int, List[Dict[str, int]]]:
    """Parsa una riga del tipo:
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    Restituisce: (game_id, [ {color: count}, ... ])
    """
    prefix, rest = line.split(":", 1)
    game_id = int(prefix.strip().split()[1])
    rounds_str = rest.strip().split(";")
    rounds: List[Dict[str, int]] = []

    for rd in rounds_str:
        rd = rd.strip()
        if not rd:
            continue
        cubes: Dict[str, int] = {}
        for part in rd.split(","):
            part = part.strip()
            if not part:
                continue
            num_str, color = part.split()
            cubes[color] = int(num_str)
        rounds.append(cubes)

    return game_id, rounds


def solve_1(test_string: Optional[str] = None) -> int:
    """Somma gli ID dei giochi che sono possibili dato MAX_CUBES."""
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        game_id, rounds = _parse_game_line(line)
        feasible = True
        for cubes in rounds:
            for color, limit in MAX_CUBES.items():
                if cubes.get(color, 0) > limit:
                    feasible = False
                    break
            if not feasible:
                break
        if feasible:
            total += game_id

    return total


def solve_2(test_string: Optional[str] = None) -> int:
    """Per ogni gioco calcola la 'power' = prodotto dei minimi cubi necessari,
    e somma tutte le power.
    """
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        _, rounds = _parse_game_line(line)
        needed: Dict[str, int] = {"red": 0, "green": 0, "blue": 0}
        for cubes in rounds:
            for color in needed:
                needed[color] = max(needed[color], cubes.get(color, 0))
        total += prod(needed.values())

    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
