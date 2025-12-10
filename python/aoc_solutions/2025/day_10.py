from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias, cast

from itertools import combinations
from functools import reduce
import operator
import numpy as np
import pulp

GI = GetInput()

Light: TypeAlias = int
Button: TypeAlias = int
Jolts: TypeAlias = list[int]
Machine: TypeAlias = tuple[Light,list[Button], Jolts]

Index: TypeAlias = int
ButtonSpec: TypeAlias = list[Index]
JoltsReq: TypeAlias = list[int]
MachineP2: TypeAlias = tuple[list[ButtonSpec], JoltsReq]


def xor_all(buttons: list[Button]) -> int:
    return reduce(operator.xor, buttons, 0)



def unique_combs(buttons: list[Button]) -> list[list[Button]]:
    n = len(buttons)
    out: list[list[Button]] = list()
    for r in range(1, n + 1):
        for combo in combinations(buttons, r):
            out.append(list(combo))
    return out

def solve_machine(machine: Machine) -> int:
    possible_results: list[list[Button]] = list()
    target: Light = machine[0]
    buttons: list[Button] = machine[1]
    
    for comb in unique_combs(buttons):
        if xor_all(comb) == target:
            possible_results.append(comb)
   

    possible_results.sort(key=lambda x: len(x))

    return len(possible_results[0])

def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    res : int = 0
    machines : list[Machine]  = list()
    for line in inputs_1.strip().splitlines():
        pieces = line.split(' ')
        tmp_light_strm2: str = pieces[0].strip('[]').replace('.', '0').replace('#', '1')
        tmp_light: Light = int(tmp_light_strm2,2)

        len_light : int = len(str(tmp_light_strm2))
        
        tmp_buttons: list[Button] = list()
        for piece in pieces[1:]:
            if "{" in piece:
                continue
            tmp_button: list[str] = ['0'] * len_light
            indexes: list[int] = [ int(el) 
                                   for el in piece.strip('()').split(",")
                                 ]
            for i in indexes:
                tmp_button[i] = '1'
            
            button: Button = int(''.join(tmp_button),2)
            tmp_buttons.append(button)
        tmp_machine: Machine = (tmp_light,tmp_buttons,[0])
        machines.append(tmp_machine)

        res += solve_machine(tmp_machine)
    
    return res

def pulp_solve(machine: MachineP2) -> int:
    """
    Risolve una singola macchina con PuLP.

    machine: (buttons, jolts)
      - buttons: lista di bottoni, ciascuno come lista di indici di luci
      - jolts:  lista di target jolts per ogni luce

    Ritorna il numero minimo di pressioni totali.
    """
    buttons, jolts = machine
    num_lights: int = len(jolts)
    num_buttons: int = len(buttons)

    # Problema di PL intera: minimizza sum(x_j)
    prob = pulp.LpProblem("MinPresses", pulp.LpMinimize)

    # x_j = quante volte premo il bottone j (interi >= 0)
    x: list[pulp.LpVariable] = [
        pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer")
        for j in range(num_buttons)
    ]

    # Obiettivo: minimizzare il totale delle pressioni
    prob += pulp.lpSum(x), "TotalPresses"

    # Vincoli: per ogni luce p, somma dei contributi dei bottoni = jolts[p]
    for p in range(num_lights):
        prob += (
            pulp.lpSum(x[j] for j in range(num_buttons) if p in buttons[j])
            == jolts[p],
            f"Jolts_light_{p}",
        )

    # Risolvi (CBC di default)
    status: int = prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if status != pulp.LpStatusOptimal:
        raise RuntimeError(f"Soluzione non ottimale o problema irrisolvibile: {pulp.LpStatus[status]}")

    raw_obj = pulp.value(prob.objective)
    if raw_obj is None:
        raise RuntimeError("Objective value is None despite optimal status")
    
    objective_val: float = cast(float, raw_obj)


    return int(round(objective_val))

def parse_machine_p2(line: str) -> MachineP2:
    """
    Parsea una riga di input in una MachineP2 = (buttons, jolts).

    Esempio riga:
      "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    """
    # Split "furbo" sugli spazi
    pieces: list[str] = line.strip().split()

    # Il pattern tra [] lo usiamo solo per sapere quante luci ci sono (check opzionale)
    indicator_raw: str = pieces[0].strip("[]")
    num_lights: int = len(indicator_raw)

    buttons: list[ButtonSpec] = []
    jolts: JoltsReq = []

    for piece in pieces[1:]:
        if piece.startswith("{"):
            # Jolts: "{3,5,4,7}" → [3, 5, 4, 7]
            jolts = [int(el) for el in piece.strip("{}").split(",")]
        elif piece.startswith("("):
            # Bottone: "(0,2,3)" → [0, 2, 3]
            idxs: list[int] = [int(el) for el in piece.strip("()").split(",")]
            buttons.append(idxs)

    # Check di consistenza (non obbligatorio, ma carino)
    if len(jolts) != num_lights:
        raise ValueError(
            f"Incoerenza: indicator ha {num_lights} luci, "
            f"ma i jolts hanno lunghezza {len(jolts)}"
        )

    return (buttons, jolts)

def solve_2(test_string: str | None = None) -> int:
    """
    Parte 2: somma le pressioni minime per tutte le macchine usando PuLP.
    """
    inputs_1: str = GI.input if test_string is None else test_string

    res: int = 0
    machines: list[MachineP2] = []

    total_lines: int = len(inputs_1.strip().splitlines())
    current: int = 0

    for line in inputs_1.strip().splitlines():
        current += 1
        machine: MachineP2 = parse_machine_p2(line)
        machines.append(machine)

        best_presses: int = pulp_solve(machine)
        res += best_presses

        # progress bar minimale
        print(
            f"Calcolato il best per {current:03} di {total_lines}: "
            f"{current / total_lines * 100:.2f}%",
            end="\r",
        )

    print()  # newline finale per non sporcare l'output
    return res


if __name__ == "__main__":
    
    test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
