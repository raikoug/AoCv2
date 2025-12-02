from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional, List, Dict
from math import factorial

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()
## info
##    cpy x y   copies x (either an integer or the value of a register) into register y.
##    inc x     increases the value of register x by one.
##    dec x     decreases the value of register x by one.
##    jnz x y   jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
##    tgl x     toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):
##    out x     (either an integer or the value of a register) as the next value for the clock signal
####  TGL
#          For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
#          For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
#          The arguments of a toggled instruction are not affected.
#          If an attempt is made to toggle an instruction outside the program, nothing happens.
#          If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
#          If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.


def _run_program(instructions: List[str], initial_eggs: int) -> bool:
    """Esegue il linguaggio Assembunny e restituisce i registri finali."""
    regs: Dict[str, int] = {"a": initial_eggs, "b": 0, "c" : 0, "d": 0}
    ip = 0
    n = len(instructions)

    result = ""

    def _value(token: str) -> int:
        return int(token) if token.lstrip("-").isdigit() else regs[token]
    
    def _check_result(result: str) -> bool:
        # return false if result is not in 010101010101 format
        if len(result) == 1:
            if result == "0":
                return True
            return False
        if set(result[0::2]) == set("0") and set(result[1::2]) == set("1"):
            return True
        return False

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
            offset = _value(offset)
            if _value(x) != 0:
                ip += int(offset)
            else:
                ip += 1
        elif op == "out":
            val = _value(parts[1])
            result += str(val)
            print(val, end = "")
            res = _check_result(result)
            if not res:
                return False
            if len(result) > 1000:
                return True
            ip += 1
        elif op == "tgl":
            ip_tochange = ip + regs[parts[1]]

            try:
                actual_instruction = instructions[ip_tochange]
            except:
                pass
            else:
                parts = actual_instruction.split()
                actual_op = parts[0]
                new_op = "_"
                if actual_op == "inc":
                    new_op = f"dec {parts[1]}"
                elif actual_op == "dec":
                    new_op = f"inc {parts[1]}"
                elif actual_op == "tgl":
                    new_op = f"inc {parts[1]}"
                elif actual_op == "jnz":
                    new_op = f"cpy {parts[1]} {parts[2]}"
                elif actual_op == "cpy":
                    new_op = f"jnz {parts[1]} {parts[2]}"
                elif actual_op == "out":
                    new_op = f"inc {parts[1]}"
                else:
                    print(f"mi sono dimenticato di: {actual_op}")
                    exit(1)
                
                instructions[ip_tochange] = new_op
            finally:
                ip += 1

        else:
            raise ValueError(f"Istruzione sconosciuta: {op!r}")

    return True


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    
    instructions: List[str] = raw.splitlines()
    initial_eggs: int = 1
    while True:
        print(f"Trye with egg {initial_eggs}: ", end= "")
        res = _run_program(instructions, initial_eggs)
        if res:
            break
        initial_eggs += 1
        print()
    
    return initial_eggs

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
