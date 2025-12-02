from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def create_disk(start: str, length: int) -> str:
    """Genera i dati sul disco fino a raggiungere almeno `length` bit."""
    data = start
    while len(data) < length:
        b = "".join("0" if ch == "1" else "1" for ch in reversed(data))
        data = f"{data}0{b}"
    return data[:length]


def checksum(data: str) -> str:
    """Calcola il checksum iterativo finché la lunghezza è dispari."""
    while len(data) % 2 == 0:
        pairs = (data[i : i + 2] for i in range(0, len(data), 2))
        data = "".join("1" if p in ("11", "00") else "0" for p in pairs)
    return data


def solve_1(test_string: Optional[str] = None) -> str:
    raw = GI.input if test_string is None else test_string
    start = raw.strip()
    disk = create_disk(start, 272)
    return checksum(disk)


def solve_2(test_string: Optional[str] = None) -> str:
    raw = GI.input if test_string is None else test_string
    start = raw.strip()
    disk = create_disk(start, 35651584)
    return checksum(disk)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
