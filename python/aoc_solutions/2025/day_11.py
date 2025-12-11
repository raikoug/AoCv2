from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput

from queue import Queue
from functools import cache

GI = GetInput()


def parse_devices(raw: str) -> dict[str, list[str]]:
    devices: dict[str, list[str]] = {}
    for line in raw.strip().splitlines():
        left, right = line.split(":", maxsplit=1)
        devices[left.strip()] = right.strip().split()
    return devices

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    devices = parse_devices(inputs_1)

    @cache
    def dfs(node: str) -> int:
        if node == "out":
            return 1
        return sum(dfs(nxt) for nxt in devices.get(node, []))

    return dfs("you")


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    devices = parse_devices(inputs_1)

    @cache
    def dfs(node: str, seen_fft: bool, seen_dac: bool) -> int:
        total = 0
        for nxt in devices.get(node, []):
            new_seen_fft = seen_fft or (nxt == "fft")
            new_seen_dac = seen_dac or (nxt == "dac")

            if nxt == "out":
                if new_seen_fft and new_seen_dac:
                    total += 1
            else:
                total += dfs(nxt, new_seen_fft, new_seen_dac)

        return total

    return dfs("svr", False, False)


if __name__ == "__main__":
    test = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    test2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
