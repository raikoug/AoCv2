from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _run_program(instructions: List[str], initial_c: int) -> Dict[str, int]:
    """Esegue il linguaggio Assembunny e restituisce i registri finali."""
    regs: Dict[str, int] = {"a": 0, "b": 0, "c": initial_c, "d": 0}
    ip = 0
    n = len(instructions)

    def _value(token: str) -> int:
        return int(token) if token.lstrip("-").isdigit() else regs[token]

    while 0 <= ip < n:
        parts = instructions[ip].split()
        op = parts[0]

        if op == "inc":
            regs[parts[1]] += 1
            ip += 1
        elif op == "dec":
            regs[parts[1]] -= 1
            ip += 1
        elif op == "cpy":
            x, y = parts[1], parts[2]
            regs[y] = _value(x)
            ip += 1
        elif op == "jnz":
            x, offset = parts[1], parts[2]
            if _value(x) != 0:
                ip += int(offset)
            else:
                ip += 1
        else:
            raise ValueError(f"Istruzione sconosciuta: {op!r}")

    return regs


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    instructions = [line for line in raw.splitlines() if line.strip()]
    regs = _run_program(instructions, initial_c=0)
    return regs["a"]


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    instructions = [line for line in raw.splitlines() if line.strip()]
    regs = _run_program(instructions, initial_c=1)
    return regs["a"]


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
