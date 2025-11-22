from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _parse_ingredients(raw: str, with_calories: bool) -> List[List[int]]:
    """Parsa le proprietà degli ingredienti.
    Ritorna una lista di [capacity, durability, flavor, texture] (+ opzionale calories).
    """
    ingredients: List[List[int]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        capacity = int(parts[2].rstrip(","))
        durability = int(parts[4].rstrip(","))
        flavor = int(parts[6].rstrip(","))
        texture = int(parts[8].rstrip(","))
        if with_calories:
            calories = int(parts[10].rstrip(","))
            ingredients.append([capacity, durability, flavor, texture, calories])
        else:
            ingredients.append([capacity, durability, flavor, texture])
    return ingredients


def _score(ingredients: List[List[int]], amounts: Tuple[int, int, int, int]) -> int:
    a, b, c, d = amounts
    cap = max(0, a * ingredients[0][0] + b * ingredients[1][0] + c * ingredients[2][0] + d * ingredients[3][0])
    dur = max(0, a * ingredients[0][1] + b * ingredients[1][1] + c * ingredients[2][1] + d * ingredients[3][1])
    fla = max(0, a * ingredients[0][2] + b * ingredients[1][2] + c * ingredients[2][2] + d * ingredients[3][2])
    tex = max(0, a * ingredients[0][3] + b * ingredients[1][3] + c * ingredients[2][3] + d * ingredients[3][3])
    return cap * dur * fla * tex


def _calories(ingredients: List[List[int]], amounts: Tuple[int, int, int, int]) -> int:
    a, b, c, d = amounts
    return (
        a * ingredients[0][4]
        + b * ingredients[1][4]
        + c * ingredients[2][4]
        + d * ingredients[3][4]
    )


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    ingredients = _parse_ingredients(raw, with_calories=False)

    best = 0
    # a + b + c + d = 100, a,b,c,d >= 0
    for a in range(101):
        for b in range(101 - a):
            for c in range(101 - a - b):
                d = 100 - a - b - c
                score = _score(ingredients, (a, b, c, d))
                if score > best:
                    best = score
    return best


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    ingredients = _parse_ingredients(raw, with_calories=True)

    best = 0
    for a in range(101):
        for b in range(101 - a):
            for c in range(101 - a - b):
                d = 100 - a - b - c
                if _calories(ingredients, (a, b, c, d)) != 500:
                    continue
                score = _score(ingredients, (a, b, c, d))
                if score > best:
                    best = score
    return best


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
