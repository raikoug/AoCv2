from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import string
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


def word_shift(word: str, key: int) -> str:
    res = ""
    for char in word:
        if char in string.ascii_lowercase:
            res += chr(((ord(char) - 97 + key) % 26) + 97)
        elif char in string.ascii_uppercase:
            res += chr(((ord(char) - 65 + key) % 26) + 65)
        else:
            res += char
    return res


def checksum(p: str) -> str:
    mapping: dict[str, int] = {}
    for char in p:
        if char in string.ascii_lowercase:
            mapping[char] = mapping.get(char, 0) + 1

    # Ordina per frequenza decrescente, poi alfabetico
    ordered = sorted(mapping.items(), key=lambda kv: (-kv[1], kv[0]))
    return "".join(ch for ch, _ in ordered[:5])


def _parse_and_filter(
    raw: str,
) -> tuple[int, list[tuple[list[str], int]]]:
    res = 0
    correct_rooms: list[tuple[list[str], int]] = []

    for line in raw.splitlines():
        if not line.strip():
            continue

        full_sector, checksum_part = line.split("[")
        expected = checksum_part.rstrip("]")
        sector_id = int(full_sector.split("-")[-1])
        name_part = "-".join(full_sector.split("-")[:-1])

        check = checksum(name_part)
        if check == expected:
            res += sector_id
            sector_words = name_part.split("-")
            correct_rooms.append((sector_words, sector_id))

    return res, correct_rooms


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res, _ = _parse_and_filter(inputs_1)
    return res


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    _, correct_rooms = _parse_and_filter(inputs_1)

    for sector_words, key in correct_rooms:
        sector = " ".join(sector_words)
        decoded = word_shift(sector, key)
        if "north" in decoded:
            return key

    raise ValueError("North pole room not found")


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
