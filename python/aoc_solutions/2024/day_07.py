from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from queue import PriorityQueue
from typing import Literal, NamedTuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()

Operation = Literal["+", "*", "||"]


@dataclass
class Equation:
    result: int
    values: list[int]
    good_ones: list[list[Operation]] = field(default_factory=list)
    ok: bool = False


class Node(NamedTuple):
    priority: int
    tmp_res: int
    index: int
    operations: list[Operation]


def parse_equations(raw: str) -> list[Equation]:
    equations: list[Equation] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        result_str, values_str = line.split(":")
        result = int(result_str)
        values = [int(el) for el in values_str.strip().split()]
        equations.append(Equation(result=result, values=values))
    return equations


def count_ok_equations(equations: list[Equation]) -> int:
    return sum(1 for eq in equations if eq.ok)


def sum_ok_equation_results(equations: list[Equation]) -> int:
    return sum(eq.result for eq in equations if eq.ok)


def evaluate_equation(eq: Equation, allow_concat: bool) -> bool:
    """
    Restituisce True se esiste una combinazione di operazioni che porta
    da eq.values al risultato eq.result.

    Usa una PriorityQueue per esplorare prima gli stati più promettenti.
    Riempie eq.good_ones con le sequenze di operazioni trovate.
    """
    values = eq.values
    target = eq.result
    length = len(values)

    if length == 0:
        return False

    q: PriorityQueue[Node] = PriorityQueue()

    # Primo nodo: nessuna operazione applicata, primo valore come risultato temporaneo
    first_value = values[0]
    q.put(Node(priority=target - first_value, tmp_res=first_value, index=0, operations=[]))

    found = False

    while not q.empty():
        priority, tmp_res, index, operations = q.get()

        # Passiamo al prossimo valore in lista
        index += 1

        # Se abbiamo consumato tutti i valori, verifichiamo il risultato
        if index == length:
            if tmp_res == target:
                eq.ok = True
                eq.good_ones.append(operations)
                found = True
            continue

        new_value = values[index]

        # Somma
        add_res = tmp_res + new_value
        if add_res <= target:
            q.put(Node(priority=target - add_res,
                       tmp_res=add_res,
                       index=index,
                       operations=operations + ["+"]))

        # Moltiplicazione
        mul_res = tmp_res * new_value
        if mul_res <= target:
            q.put(Node(priority=target - mul_res,
                       tmp_res=mul_res,
                       index=index,
                       operations=operations + ["*"]))

        # Concatenazione (solo se consentita)
        if allow_concat:
            concat_res = int(f"{tmp_res}{new_value}")
            if concat_res <= target:
                q.put(Node(priority=target - concat_res,
                           tmp_res=concat_res,
                           index=index,
                           operations=operations + ["||"]))

    return found


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    equations = parse_equations(inputs_1)
    for eq in equations:
        evaluate_equation(eq, allow_concat=False)

    return sum_ok_equation_results(equations)


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    equations = parse_equations(inputs_1)
    for eq in equations:
        evaluate_equation(eq, allow_concat=True)

    return sum_ok_equation_results(equations)


if __name__ == "__main__":
    test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

    # Input reale da Advent of Code
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test locale:
    # print(f\"Part 1 (test): {solve_1(test)}\")
    # print(f\"Part 2 (test): {solve_2(test)}\")
