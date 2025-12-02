from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string

    total_code = 0
    total_memory = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        code_len = len(line)
        total_code += code_len
        memory_str = eval(line)
        total_memory += len(memory_str)

    return total_code - total_memory


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string

    total_code = 0
    total_encoded = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        code_len = len(line)
        total_code += code_len

        encoded_line = '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'
        total_encoded += len(encoded_line)

    return total_encoded - total_code


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
