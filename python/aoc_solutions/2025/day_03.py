from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput

GI = GetInput()

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res = 0
    for line in inputs_1.strip().splitlines():
        numbers = ([
            int(el) for el in line
        ])
        
        idx1 = numbers.index(max(numbers[:-1]))
        high1 = numbers[idx1]
        idx2 = numbers.index(max(numbers[idx1+1:]))
        high2 = numbers[idx2]
        res += int(str(high1)+str(high2))

    return res

def slice_inclusive(s: list[int], start: int, end: int) -> list[int]:
    return s[start:end + 1]

def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res = 0
    K = 12
    for line in inputs_1.strip().splitlines():
        numbers = ([
            int(el) for el in line
        ])
        n = len(numbers)

        start = 0
        remaining = K
        meta_digits: list[str] = []

        while remaining > 0:
            stop = n - (remaining - 1)

            window = numbers[start:stop]
            best = max(window)
            local_idx = window.index(best)
            idx = start + local_idx

            meta_digits.append(str(best))
            start = idx + 1
            remaining -= 1

        meta = "".join(meta_digits)
        res += int(meta)
        
    return res


if __name__ == "__main__":
    test = """987654321111111
811111111111119
234234234234278
818181911112111"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
