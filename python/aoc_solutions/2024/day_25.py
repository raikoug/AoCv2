from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


# ---------------------------------------------------------------------------
# Helpers per lock e key
# ---------------------------------------------------------------------------

def eval_key(lines: List[str]) -> List[int]:
    """
    Converte la rappresentazione di una chiave in una lista di altezze per colonna.

    Esempio (h = 7):

        ..... 6
        ..... 5
        ..... 4
        #.... 3
        #.#.. 2
        #.#.# 1
        ##### 0

    Il valore per ogni colonna è "quanti # sopra il bordo in basso".
    """
    h = len(lines)
    w = len(lines[0])
    res: List[int] = [0] * w

    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == "#":
                # distanza dal basso (riga 0 in basso)
                res[col] = max(res[col], h - row - 1)

    return res


def eval_lock(lines: List[str]) -> List[int]:
    """
    Converte la rappresentazione di un lucchetto in una lista di altezze per colonna.

    Esempio (h = 7):

        ##### 0
        .#### 1
        .#### 2
        .#### 3
        .#.#. 4
        .#... 5
        ..... 6

    Il valore per ogni colonna è "quanti # sotto il bordo in alto".
    """
    h = len(lines)
    w = len(lines[0])
    res: List[int] = [0] * w

    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == "#":
                # distanza dall'alto (riga 0 in alto)
                res[col] = max(res[col], row)

    return res


def sum_lock_key(lock: List[int], key: List[int]) -> List[int]:
    return [lock[i] + key[i] for i in range(len(lock))]


def eval_block(block: List[str]) -> Tuple[List[int], bool]:
    """
    Analizza un blocco (lock o key) e restituisce:
      - la lista delle altezze
      - un bool: True se è un lock, False se è una key

    Convenzione del puzzle:
      - se la prima riga è "#####..." → è un lock
      - se l'ultima riga è "#####..." → è una key
    """
    if block[0].startswith("#"):
        return eval_lock(block), True
    else:
        return eval_key(block), False


def is_ok(fit: List[int], max_height: int = 5) -> bool:
    """
    Ritorna True se tutte le colonne rispettano il limite di altezza max_height.
    (Nel puzzle: non devono superare la camera interna.)
    """
    return all(el <= max_height for el in fit)


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string

    locks: List[List[int]] = []
    keys: List[List[int]] = []

    tmp_block: List[str] = []

    def flush_block() -> None:
        nonlocal tmp_block
        if not tmp_block:
            return
        pins, is_lock = eval_block(tmp_block)
        if is_lock:
            locks.append(pins)
        else:
            keys.append(pins)
        tmp_block = []

    for line in raw.splitlines():
        line = line.strip()
        if line:
            tmp_block.append(line)
        else:
            flush_block()

    # ultimo blocco (se l'input non termina con una riga vuota)
    flush_block()

    result = 0
    for key in keys:
        for lock in locks:
            if is_ok(sum_lock_key(lock, key)):
                result += 1

    return result


# ---------------------------------------------------------------------------
# Part 2 (stub: Day 25 ha solo una parte)
# ---------------------------------------------------------------------------

def solve_2(test_string: str | None = None) -> int:
    """
    AoC 2024 Day 25 ha solo Part 1.
    Manteniamo questa funzione per coerenza con il template.
    """
    return 0


if __name__ == "__main__":
    test = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

    print(f"Part 1 (test): {solve_1(test)}")
    print(f"Part 1 (input reale): {solve_1()}")
    print(f"Part 2 (stub): {solve_2()}")
