from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


@dataclass
class Disk:
    number: int
    module: int
    initial: int
    state: int

    def __init__(self, number: int, module: int, initial: int) -> None:
        self.number = number
        self.module = module
        self.initial = initial
        self.state = initial
        # offset iniziale in base alla posizione nel sistema
        self.rotate(number)

    def rotate(self, steps: int) -> None:
        self.state = (self.state + steps) % self.module


def _parse_disks(raw: str, extra_disk: bool) -> List[Disk]:
    disks: List[Disk] = []
    lines = [line for line in raw.splitlines() if line.strip()]
    for line in lines:
        parts = line.split()
        number = int(parts[1].lstrip("#"))
        module = int(parts[3])
        initial = int(parts[-1].rstrip("."))
        disks.append(Disk(number, module, initial))

    if extra_disk:
        disks.append(Disk(len(disks) + 1, 11, 0))

    return disks


def _find_time(disks: List[Disk]) -> int:
    time = 0
    while True:
        time += 1
        states = []
        for disk in disks:
            disk.rotate(1)
            states.append(disk.state)
        if all(state == 0 for state in states):
            return time


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    disks = _parse_disks(raw, extra_disk=False)
    return _find_time(disks)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    disks = _parse_disks(raw, extra_disk=True)
    return _find_time(disks)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
