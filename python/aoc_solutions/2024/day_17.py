from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Registers = Dict[str, int]
Program = List[int]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_input(raw: str) -> tuple[Registers, Program]:
    """
    Input tipo:

        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0
    """
    regs: Registers = {"A": 0, "B": 0, "C": 0}
    program: Program = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Register"):
            _, reg, val = line.split()
            reg = reg.rstrip(":")
            regs[reg] = int(val)
        elif line.startswith("Program:"):
            _, instr = line.split()
            program = [int(x) for x in instr.split(",")]

    if not program:
        raise ValueError("Program non trovato nell'input")

    return regs, program


# ---------------------------------------------------------------------------
# VM / interpreter
# ---------------------------------------------------------------------------

def run_program(program: Program, regs: Registers, max_outputs: int | None = None) -> List[int]:
    """
    Esegue il program con i registri dati, secondo le regole del day 17.

    Se max_outputs è valorizzato, si ferma appena produce più di max_outputs
    valori di output (utile per pruning nella parte 2).
    """
    # Copia per non mutare il dict originale
    R: Registers = {"A": regs["A"], "B": regs["B"], "C": regs["C"]}

    def get_operand(value: int) -> int:
        # combo operand
        if value < 4:
            return value
        if value == 4:
            return R["A"]
        if value == 5:
            return R["B"]
        if value == 6:
            return R["C"]
        # 7 è "reserved" e non dovrebbe comparire
        raise ValueError(f"Combo operand non valido: {value}")

    ip = 0
    out: List[int] = []

    while 0 <= ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1] if ip + 1 < len(program) else 0

        if opcode == 0:  # ADV
            R["A"] = R["A"] // (2 ** get_operand(operand))
            ip += 2
        elif opcode == 1:  # BXL
            R["B"] = R["B"] ^ operand
            ip += 2
        elif opcode == 2:  # BST
            R["B"] = get_operand(operand) % 8
            ip += 2
        elif opcode == 3:  # JNZ
            if R["A"] != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # BCX
            R["B"] = R["B"] ^ R["C"]
            ip += 2
        elif opcode == 5:  # OUT
            out.append(get_operand(operand) % 8)
            ip += 2
            if max_outputs is not None and len(out) > max_outputs:
                break
        elif opcode == 6:  # BDV
            R["B"] = R["A"] // (2 ** get_operand(operand))
            ip += 2
        elif opcode == 7:  # CDV
            R["C"] = R["A"] // (2 ** get_operand(operand))
            ip += 2
        else:
            raise ValueError(f"Opcode sconosciuto: {opcode}")

    return out


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> str:
    """
    Part 1 chiede proprio la stringa CSV dell'output (non un int).
    """
    raw = GI.input if test_string is None else test_string
    regs, program = parse_input(raw)

    out = run_program(program, regs)
    return ",".join(str(x) for x in out)


# ---------------------------------------------------------------------------
# Part 2 – trova A minimo tale che out(A) == program
# ---------------------------------------------------------------------------

def find_minimum_A_self_reproducing(regs: Registers, program: Program) -> int:
    """
    Implementa il backtracking in base 8 usato da molte soluzioni:

    - Costruiamo A in base 8 dall'ultima cifra verso la prima.
    - A ogni passo fissiamo una cifra in più (moltiplicando per 8 e
      testando i 8 possibili valori successivi).
    - Per livello nrem usiamo come target la *coda* del programma:
        target = program[nrem - 1:]
      (es: nrem = len(program) -> solo l'ultimo elemento,
           nrem = 1            -> tutto il programma)
    - Ci fermiamo al primo A che riproduce l'intero programma.
    """

    def enumerate_candidates(prefix: int, target: List[int]) -> List[int]:
        """
        Per un prefisso 'prefix', prova A in [prefix*8 .. prefix*8+7]
        e ritorna quelli per cui run_program(A) == target.
        """
        base = prefix * 8
        candidates: List[int] = []
        for a in range(base, base + 8):
            local_regs = dict(regs)
            local_regs["A"] = a
            out = run_program(program, local_regs)
            if out == target:
                candidates.append(a)
        return candidates

    sys.setrecursionlimit(10_000)

    def dfs(prefix: int, nrem: int) -> int | None:
        if nrem == 0:
            return prefix

        # Suffix del programma dalla posizione nrem-1 in poi
        target_suffix = program[nrem - 1 :]

        for cand in enumerate_candidates(prefix, target_suffix):
            res = dfs(cand, nrem - 1)
            if res is not None:
                return res
        return None

    n = len(program)
    result = dfs(0, n)
    if result is None:
        raise RuntimeError("Nessun valore di A trovato che riproduca il programma.")
    return result


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    regs, program = parse_input(raw)
    return find_minimum_A_self_reproducing(regs, program)


if __name__ == "__main__":
    test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    print(f"Part 1 (test): {solve_1(test)}")
    print(f"Part 1 (input): {solve_1()}")
    print(f"Part 2 (input): {solve_2()}")
