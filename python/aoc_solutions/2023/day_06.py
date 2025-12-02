from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _parse_races(raw: str) -> List[Tuple[int, int]]:
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    if len(lines) < 2:
        return []
    times = [int(x) for x in lines[0].split()[1:]]
    dists = [int(x) for x in lines[1].split()[1:]]
    return list(zip(times, dists))


def _count_ways_bruteforce(time: int, distance: int) -> int:
    """Conta i modi per battere il record iterando tutti i possibili hold-time."""
    count = 0
    for hold in range(1, time):
        if hold * (time - hold) > distance:
            count += 1
    return count


def _count_ways_math(time: int, distance: int) -> int:
    """
    Conta i modi per battere il record in modo efficiente, usando una ricerca binaria
    sugli hold-time validi. Utile per i numeri molto grandi della parte 2.
    """
    if time <= 10_000:
        return _count_ways_bruteforce(time, distance)

    def first_ok() -> int:
        lo, hi = 0, time
        while lo < hi:
            mid = (lo + hi) // 2
            if mid * (time - mid) > distance:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def last_ok() -> int:
        lo, hi = 0, time
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid * (time - mid) > distance:
                lo = mid
            else:
                hi = mid - 1
        return lo

    start = first_ok()
    end = last_ok()
    return max(0, end - start + 1)


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    races = _parse_races(raw)
    result = 1
    for time, dist in races:
        result *= _count_ways_bruteforce(time, dist)
    return result


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    if len(lines) < 2:    
    return 0
    big_time = int("".join(lines[0].split()[1:]))
    big_dist = int("".join(lines[1].split()[1:]))
    return _count_ways_math(big_time, big_dist)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
