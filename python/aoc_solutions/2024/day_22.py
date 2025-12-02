from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, cast

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

MOD = 16_777_216  # 2^24
DeltaKey = Tuple[int, int, int, int]


# ---------------------------------------------------------------------------
# Generatore di numeri segreti
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def next_secret(secret: int) -> int:
    """
    Trasforma il numero segreto secondo le tre fasi del puzzle:
      1. secret = ((secret * 64) ^ secret) % MOD
      2. secret = ((secret // 32) ^ secret) % MOD
      3. secret = ((secret * 2048) ^ secret) % MOD
    """
    s = secret
    s = ((s * 64) ^ s) % MOD
    s = ((s // 32) ^ s) % MOD
    s = ((s * 2048) ^ s) % MOD
    return s


def final_secret_after(secret: int, steps: int = 2000) -> int:
    """
    Applica `next_secret` `steps` volte e ritorna il valore finale.
    Questa funzione NON è cachata: il caching è sul singolo passo.
    """
    s = secret
    for _ in range(steps):
        s = next_secret(s)
    return s


def iter_secrets(initial: int, steps: int) -> Iterable[int]:
    """
    Genera `steps` numeri segreti successivi a partire da `initial`.
    """
    s = initial
    for _ in range(steps):
        s = next_secret(s)
        yield s


# ---------------------------------------------------------------------------
# Part 2 – Analisi delle sequenze di differenze di prezzo
# ---------------------------------------------------------------------------

def analyse_buyer(initial: int, steps: int = 2000) -> Dict[DeltaKey, int]:
    """
    Per un singolo numero iniziale:

    - Genera i `steps` numeri segreti.
    - Ad ogni passo considera la cifra delle unità come "prezzo" (secret % 10).
    - Calcola le differenze tra prezzi consecutivi (Δprice).
    - Considera tutte le sequenze di 4 differenze consecutive.
    - Per OGNI sequenza, tiene solo la PRIMA volta che appare per questo buyer,
      associandole il prezzo di quel momento.

    Ritorna un dict:
      { (d1, d2, d3, d4): prezzo_alla_prima_occorrenza }
    """
    # Prezzo iniziale: dalla secret di partenza
    s = initial
    prev_price = s % 10

    recent_deltas: List[int] = []
    first_seen: Dict[DeltaKey, int] = {}

    for secret in iter_secrets(initial, steps):
        price = secret % 10
        delta = price - prev_price
        prev_price = price

        recent_deltas.append(delta)
        if len(recent_deltas) > 4:
            recent_deltas.pop(0)

        if len(recent_deltas) == 4:
            key = cast(DeltaKey, tuple(recent_deltas))
            if key not in first_seen:
                first_seen[key] = price

    return first_seen


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    initials = [int(line) for line in raw.splitlines() if line.strip()]

    total = 0
    for initial in initials:
        total += final_secret_after(initial, 2000)

    return total


# ---------------------------------------------------------------------------
# Part 2
# ---------------------------------------------------------------------------

def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    initials = [int(line) for line in raw.splitlines() if line.strip()]

    # pattern -> somma delle banane guadagnate su TUTTI i buyer
    global_scores: Dict[DeltaKey, int] = {}

    for initial in initials:
        first_seen = analyse_buyer(initial)
        for key, price in first_seen.items():
            global_scores[key] = global_scores.get(key, 0) + price

    return max(global_scores.values()) if global_scores else 0


if __name__ == "__main__":
    test = """1
10
100
2024
"""
    print(f"Part 1 (test): {solve_1(test)}")
    print(f"Part 1 (input): {solve_1()}")
    print(f"Part 2 (input): {solve_2()}")
