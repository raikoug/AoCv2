from __future__ import annotations

from pathlib import Path
from typing import Any, List, Sequence, TypeVar
import sys

# Se non lo usi, puoi eliminare questa import
# from itertools import permutations


T = TypeVar("T")

Rule = tuple[int, int]
Rules = list[Rule]
Update = list[int]
Updates = list[Update]


def safe_index(lst: Sequence[T], element: T) -> int:
    """Ritorna l'indice dell'elemento o -1 se non trovato."""
    try:
        return lst.index(element)  # type: ignore[attr-defined]
    except ValueError:
        return -1


def update_is_ok(update: Update, rules: Rules) -> bool:
    for rule in rules:
        a, b = safe_index(update, rule[0]), safe_index(update, rule[1])
        if a < 0 or b < 0:
            # number missing, ignore rule
            continue
        if a > b:
            return False

    return True


def fix_update(update: Update, rules: Rules) -> Update:
    """
    Sistemazione ricorsiva dell'update fino a quando tutte
    le regole sono rispettate. Ritorna una nuova lista ordinata.
    """
    # Lavoriamo su una copia per evitare side-effect esterni
    upd = list(update)

    for rule in rules:
        a, b = safe_index(upd, rule[0]), safe_index(upd, rule[1])
        if a < 0 or b < 0:
            # number missing, ignore rule
            continue
        if a > b:
            # swap e ricomincia il controllo
            upd[a], upd[b] = upd[b], upd[a]
            return fix_update(upd, rules)

    return upd


# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    rules: Rules = []
    updates: Updates = []

    for line in inputs_1.splitlines():
        if "|" in line:
            a_str, b_str = line.split("|")
            rules.append((int(a_str), int(b_str)))
        elif "," in line:
            tmp_upd: Update = []
            for el in line.split(","):
                tmp_upd.append(int(el))
            updates.append(tmp_upd)

    total: int = 0
    for update in updates:
        if update_is_ok(update, rules):
            total += update[len(update) // 2]
    return total


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    rules: Rules = []
    updates: Updates = []

    for line in inputs_1.splitlines():
        if "|" in line:
            a_str, b_str = line.split("|")
            rules.append((int(a_str), int(b_str)))
        elif "," in line:
            tmp_upd: Update = []
            for el in line.split(","):
                tmp_upd.append(int(el))
            updates.append(tmp_upd)

    total: int = 0
    for update in updates:
        if not update_is_ok(update, rules):
            fixed_update = fix_update(update, rules)
            total += fixed_update[len(fixed_update) // 2]
    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
