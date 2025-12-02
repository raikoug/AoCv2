from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

MASK = 0xFFFF


def _parse_wires(raw: str) -> Dict[str, str]:
    wires: Dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        expr, dest = line.split(" -> ")
        wires[dest] = expr
    return wires


def _is_number(token: str) -> bool:
    return token.isdigit()


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    wires = _parse_wires(raw)

    @lru_cache(maxsize=None)
    def eval_wire(w: str) -> int:
        if _is_number(w):
            return int(w) & MASK

        expr = wires[w]
        tokens = expr.split()

        if len(tokens) == 1:
            val = eval_wire(tokens[0])
            return val & MASK

        if len(tokens) == 2:
            op, arg = tokens
            if op != "NOT":
                raise ValueError(f"Operatore unario sconosciuto: {op!r}")
            val = ~eval_wire(arg)
            return val & MASK

        if len(tokens) == 3:
            left, op, right = tokens
            a = eval_wire(left) if not _is_number(left) else int(left)
            b = eval_wire(right) if not _is_number(right) else int(right)

            if op == "AND":
                val = a & b
            elif op == "OR":
                val = a | b
            elif op == "LSHIFT":
                val = a << b
            elif op == "RSHIFT":
                val = a >> b
            else:
                raise ValueError(f"Operatore binario sconosciuto: {op!r}")

            return val & MASK

        raise ValueError(f"Espressione non valida per {w!r}: {expr!r}")

    return eval_wire("a")


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    wires = _parse_wires(raw)

    @lru_cache(maxsize=None)
    def eval_wire_1(w: str) -> int:
        if _is_number(w):
            return int(w) & MASK

        expr = wires[w]
        tokens = expr.split()

        if len(tokens) == 1:
            val = eval_wire_1(tokens[0])
            return val & MASK

        if len(tokens) == 2:
            op, arg = tokens
            if op != "NOT":
                raise ValueError(f"Operatore unario sconosciuto: {op!r}")
            val = ~eval_wire_1(arg)
            return val & MASK

        if len(tokens) == 3:
            left, op, right = tokens
            a = eval_wire_1(left) if not _is_number(left) else int(left)
            b = eval_wire_1(right) if not _is_number(right) else int(right)

            if op == "AND":
                val = a & b
            elif op == "OR":
                val = a | b
            elif op == "LSHIFT":
                val = a << b
            elif op == "RSHIFT":
                val = a >> b
            else:
                raise ValueError(f"Operatore binario sconosciuto: {op!r}")

            return val & MASK

        raise ValueError(f"Espressione non valida per {w!r}: {expr!r}")

    a_value = eval_wire_1("a")

    wires2 = dict(wires)
    wires2["b"] = str(a_value)

    @lru_cache(maxsize=None)
    def eval_wire_2(w: str) -> int:
        if _is_number(w):
            return int(w) & MASK

        expr = wires2[w]
        tokens = expr.split()

        if len(tokens) == 1:
            val = eval_wire_2(tokens[0])
            return val & MASK

        if len(tokens) == 2:
            op, arg = tokens
            if op != "NOT":
                raise ValueError(f"Operatore unario sconosciuto: {op!r}")
            val = ~eval_wire_2(arg)
            return val & MASK

        if len(tokens) == 3:
            left, op, right = tokens
            a = eval_wire_2(left) if not _is_number(left) else int(left)
            b = eval_wire_2(right) if not _is_number(right) else int(right)

            if op == "AND":
                val = a & b
            elif op == "OR":
                val = a | b
            elif op == "LSHIFT":
                val = a << b
            elif op == "RSHIFT":
                val = a >> b
            else:
                raise ValueError(f"Operatore binario sconosciuto: {op!r}")

            return val & MASK

        raise ValueError(f"Espressione non valida per {w!r}: {expr!r}")

    return eval_wire_2("a")


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
