from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional, List, Dict

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

## info
##    cpy x y copies x (either an integer or the value of a register) into register y.
##    inc x increases the value of register x by one.
##    dec x decreases the value of register x by one.
##    jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
##    tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):

#          For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
#          For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
#          The arguments of a toggled instruction are not affected.
#          If an attempt is made to toggle an instruction outside the program, nothing happens.
#          If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
#          If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.


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
    # TODO: implementare la logica della parte 1 (assembunny / esecuzione istruzioni)
    # Usa `raw.splitlines()` per ottenere le istruzioni.
    return 0


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    # TODO: implementare la logica della parte 2
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
