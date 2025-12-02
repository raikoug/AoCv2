from __future__ import annotations

from pathlib import Path
import sys
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


@dataclass(frozen=True)
class NumberSpan:
    row: int
    col_start: int
    col_end: int  # inclusivo
    value: int


_NEIGHBORS: Tuple[Tuple[int, int], ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def _parse_grid(raw: str) -> List[str]:
    return [line.rstrip("\n") for line in raw.splitlines() if line]


def _find_numbers(grid: List[str]) -> Tuple[List[NumberSpan], Dict[Tuple[int, int], int]]:
    """Restituisce:
    - lista di NumberSpan
    - mappa (row, col) -> indice in lista NumberSpan
    """
    numbers: List[NumberSpan] = []
    pos_to_index: Dict[Tuple[int, int], int] = {}
    if not grid:
        return numbers, pos_to_index

    height = len(grid)
    width = len(grid[0])

    for r in range(height):
        c = 0
        row_str = grid[r]
        while c < width:
            ch = row_str[c]
            if ch.isdigit():
                start = c
                digits = [ch]
                c += 1
                while c < width and row_str[c].isdigit():
                    digits.append(row_str[c])
                    c += 1
                end = c - 1
                value = int("".join(digits))
                idx = len(numbers)
                span = NumberSpan(row=r, col_start=start, col_end=end, value=value)
                numbers.append(span)
                for cc in range(start, end + 1):
                    pos_to_index[(r, cc)] = idx
            else:
                c += 1

    return numbers, pos_to_index


def _is_adjacent_to_symbol(span: NumberSpan, grid: List[str]) -> bool:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    r = span.row

    for c in range(span.col_start, span.col_end + 1):
        for dr, dc in _NEIGHBORS:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < height and 0 <= cc < width:
                ch = grid[rr][cc]
                if not ch.isdigit() and ch != ".":
                    return True
    return False


def solve_1(test_string: Optional[str] = None) -> int:
    """Somma tutti i 'part numbers' adiacenti ad almeno un simbolo."""
    raw = GI.input if test_string is None else test_string
    grid = _parse_grid(raw)
    numbers, _ = _find_numbers(grid)
    return sum(span.value for span in numbers if _is_adjacent_to_symbol(span, grid))


def solve_2(test_string: Optional[str] = None) -> int:
    """Somma tutti i gear ratio: per ogni '*' che tocca esattamente due numeri,
    moltiplica i due numeri e somma i risultati.
    """
    raw = GI.input if test_string is None else test_string
    grid = _parse_grid(raw)
    numbers, pos_to_index = _find_numbers(grid)
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    total = 0
    for r in range(height):
        for c in range(width):
            if grid[r][c] != "*":
                continue
            adjacent_indices: set[int] = set()
            for dr, dc in _NEIGHBORS:
                rr = r + dr
                cc = c + dc
                if (rr, cc) in pos_to_index:
                    adjacent_indices.add(pos_to_index[(rr, cc)])
            if len(adjacent_indices) == 2:
                i1, i2 = sorted(adjacent_indices)
                total += numbers[i1].value * numbers[i2].value

    return total


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
