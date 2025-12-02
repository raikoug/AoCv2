from __future__ import annotations

from pathlib import Path
from typing import List

import sys

import numpy as np

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _parse_input(raw: str) -> List[np.ndarray]:
    """
    Converte l'input in una lista di pattern 2D, rappresentati come array numpy
    di 0/1 ('.' -> 0, '#' -> 1).
    """
    blocks = raw.strip().split("\n\n")
    patterns: List[np.ndarray] = []
    for block in blocks:
        lines = block.splitlines()
        arr = np.array([[ ".#".index(ch) for ch in line ] for line in lines], dtype=int)
        patterns.append(arr)
    return patterns


def _find_reflection_score(pattern: np.ndarray, mismatches_allowed: int) -> int:
    """
    Restituisce il punteggio della riga/colonna di riflessione:
    - 100 * riga per una riflessione orizzontale
    - colonna per una riflessione verticale

    `mismatches_allowed`:
        - 0 per la parte 1 (riflessione perfetta)
        - 1 per la parte 2 (esattamente uno "smudge")
    """
    current = pattern
    for axis_score in (100, 1):
        rows = current.shape[0]
        for split_row in range(1, rows):
            # Somma delle differenze tra coppie di righe specchiate rispetto a split_row
            diff = 0
            max_delta = min(split_row, rows - split_row)
            for delta in range(max_delta):
                upper = current[split_row - delta - 1]
                lower = current[split_row + delta]
                diff += (upper != lower).sum()
                if diff > mismatches_allowed:
                    break
            if diff == mismatches_allowed:
                return axis_score * split_row

        # Ruota di 90° in senso orario per riutilizzare la stessa logica sulle colonne
        current = np.rot90(current, -1)

    raise ValueError("Nessuna linea di riflessione trovata per il pattern fornito.")


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    patterns = _parse_input(raw)
    return sum(_find_reflection_score(p, mismatches_allowed=0) for p in patterns)


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    patterns = _parse_input(raw)
    return sum(_find_reflection_score(p, mismatches_allowed=1) for p in patterns)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
