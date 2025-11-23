from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Range = Tuple[int, int]
MAX_IP = 2 ** 32 - 1


def _parse_ranges(raw: str) -> List[Range]:
    ranges: List[Range] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        start_s, end_s = line.split("-")
        ranges.append((int(start_s), int(end_s)))
    return ranges


def _merge_ranges(ranges: List[Range]) -> List[Range]:
    """Unisce intervalli [start, end] sovrapposti o adiacenti."""
    if not ranges:
        return []

    ranges.sort(key=lambda r: r[0])
    merged: List[List[int]] = [[ranges[0][0], ranges[0][1]]]

    for start, end in ranges[1:]:
        last = merged[-1]
        if start <= last[1] + 1:
            if end > last[1]:
                last[1] = end
        else:
            merged.append([start, end])

    return [(s, e) for s, e in merged]


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    ranges = _merge_ranges(_parse_ranges(raw))

    candidate = 0
    for start, end in ranges:
        if candidate < start:
            break
        if start <= candidate <= end:
            candidate = end + 1

    return candidate


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    ranges = _merge_ranges(_parse_ranges(raw))

    allowed = 0
    prev_end = -1

    for start, end in ranges:
        if start > prev_end + 1:
            allowed += start - (prev_end + 1)
        if end > prev_end:
            prev_end = end

    if prev_end < MAX_IP:
        allowed += MAX_IP - prev_end

    return allowed


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
