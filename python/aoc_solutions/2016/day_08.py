from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()
CURRENT_DAY = int(Path(__file__).stem.replace("day_", ""))


class Digital:
    def __init__(self, rows: int = 6, cols: int = 50, on: str = "#", off: str = " ") -> None:
        self.grid: list[list[str]] = []
        self.on = on
        self.off = off
        for _ in range(rows):
            self.grid.append([self.off] * cols)

    def printa(self) -> None:
        print(self.render())

    def rect(self, length: int, height: int) -> None:
        for row in range(height):
            self.grid[row][:length] = [self.on] * length

    def row_rotate(self, row: int, times: int) -> None:
        times %= len(self.grid[row])
        self.grid[row] = self.grid[row][-times:] + self.grid[row][:-times]

    def col_rotate(self, col: int, times: int) -> None:
        column = [self.grid[i][col] for i in range(len(self.grid))]
        times %= len(column)
        column = column[-times:] + column[:-times]
        for i in range(len(self.grid)):
            self.grid[i][col] = column[i]

    def count(self) -> int:
        return sum(row.count(self.on) for row in self.grid)

    def render(self) -> str:
        return "\n".join("".join(row) for row in self.grid)


def _run_program(raw: str) -> Digital:
    d = Digital()
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("rect"):
            _, vals = line.split(" ")
            length, height = vals.split("x")
            d.rect(int(length), int(height))
        elif "column" in line:
            # rotate column x=1 by 1
            _, _, xeq, _, times = line.split(" ")
            col = int(xeq.replace("x=", ""))
            d.col_rotate(col, int(times))
        elif "row" in line:
            # rotate row y=0 by 4
            _, _, yeq, _, times = line.split(" ")
            row = int(yeq.replace("y=", ""))
            d.row_rotate(row, int(times))
    return d


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    d = _run_program(inputs_1)
    return d.count()


def solve_2(test_string: Optional[str] = None) -> str:
    inputs_1 = GI.input if test_string is None else test_string
    d = _run_program(inputs_1)
    # Ritorniamo la rappresentazione del display; la lettura "umana" la fai guardando l'output
    return d.render()


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print("Part 2:")
    print(solve_2())
