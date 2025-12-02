from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _rotate_platform(platform: List[str]) -> List[str]:
    """
    Ruota la piattaforma 90° in senso orario.
    """
    return ["".join(col) for col in zip(*platform[::-1])]


def _tilt_line_right(line: str) -> str:
    """
    "Inclina" una riga verso destra: le pietre 'O' rotolano fino a incontrare
    un muro '#' o il bordo, preservando l'ordine relativo interno al segmento.
    """
    segments = line.split("#")
    new_segments: List[str] = []

    for segment in segments:
        if not segment:
            new_segments.append(segment)
            continue
        rocks = segment.count("O")
        rock_str = "O" * rocks
        # Metti le 'O' a destra, riempiendo a sinistra con '.'
        new_segments.append(rock_str.rjust(len(segment), "."))

    return "#".join(new_segments)


def _tilt_right(platform: List[str]) -> List[str]:
    """
    Applica l'inclinazione verso destra a tutte le righe della piattaforma.
    """
    return [_tilt_line_right(row) for row in platform]


def _cycle(platform: List[str]) -> List[str]:
    """
    Esegue un ciclo completo:
    - north
    - west
    - south
    - east

    L'implementazione ruota la piattaforma e inclina sempre verso destra,
    come nel vecchio codice.
    """
    current = platform
    for _ in range(4):
        current = _tilt_right(current)
        current = _rotate_platform(current)
    return current


def _load(platform: List[str]) -> int:
    """
    Calcola il carico totale (load) delle pietre 'O' viste "da nord".
    La piattaforma è già ruotata come nell'implementazione originale,
    quindi basta sommare (indice+1) per ogni 'O' in ogni riga.
    """
    total = 0
    for row in platform:
        total += sum(idx + 1 for idx, ch in enumerate(row) if ch == "O")
    return total


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = raw.splitlines()

    # Ruotiamo per avere il "nord" a destra, come nel codice originale.
    platform = ["".join(col) for col in zip(*lines[::-1])]

    tilted = _tilt_right(platform)
    return _load(tilted)


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = raw.splitlines()

    platform = ["".join(col) for col in zip(*lines[::-1])]
    cycles = 1_000_000_000

    seen: Dict[Tuple[str, ...], int] = {}
    sequence: List[List[str]] = []

    current = platform
    step = 0

    while True:
        key = tuple(current)
        if key in seen:
            cycle_start = seen[key]
            cycle_length = step - cycle_start
            break
        seen[key] = step
        sequence.append(current)
        current = _cycle(current)
        step += 1

    # Ora conosciamo inizio e lunghezza del ciclo
    if cycles < len(sequence):
        final_platform = sequence[cycles]
    else:
        offset = (cycles - cycle_start) % cycle_length
        final_platform = sequence[cycle_start + offset]

    return _load(final_platform)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
