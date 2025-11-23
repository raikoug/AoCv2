from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


def _columns_from_rows(rows: list[str]) -> list[list[str]]:
    columns: list[list[str]] = [[] for _ in range(len(rows[0]))]
    for row in rows:
        for i, ch in enumerate(row):
            columns[i].append(ch)
    return columns


def solve_1(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    rows = [line.strip() for line in inputs_1.splitlines() if line.strip()]
    columns = _columns_from_rows(rows)

    result = ""
    for column in columns:
        best = column[0]
        best_count = column.count(best)
        for ch in column[1:]:
            cnt = column.count(ch)
            if cnt > best_count:
                best = ch
                best_count = cnt
        result += best
    return result


def solve_2(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    rows = [line.strip() for line in inputs_1.splitlines() if line.strip()]
    columns = _columns_from_rows(rows)

    result = ""
    for column in columns:
        best = column[0]
        best_count = column.count(best)
        for ch in column[1:]:
            cnt = column.count(ch)
            if cnt < best_count:
                best = ch
                best_count = cnt
        result += best
    return result


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
