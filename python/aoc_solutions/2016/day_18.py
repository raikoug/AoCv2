from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


TRAP_PATTERNS = {"^^.", ".^^", "^..", "..^"}


def new_row(row: str) -> str:
    tmp_row = "." + row + "."
    triples = (tmp_row[i : i + 3] for i in range(len(row)))
    return "".join("^" if t in TRAP_PATTERNS else "." for t in triples)


def _count_safe_tiles(first_row: str, total_rows: int) -> int:
    row = first_row
    safe = row.count(".")
    for _ in range(total_rows - 1):
        row = new_row(row)
        safe += row.count(".")
    return safe


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    first_row = raw.strip()
    return _count_safe_tiles(first_row, 40)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    first_row = raw.strip()
    return _count_safe_tiles(first_row, 400_000)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
