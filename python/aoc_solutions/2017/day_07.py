from __future__ import annotations
from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import Optional, Union
from dataclasses import dataclass, field

GI = GetInput()

@dataclass
class Node:
    name: str
    weight: int
    upper: set[str]
    lower: set[str] = field(default_factory=set)



def solve_1(test_string: str | None = None) -> tuple[dict, str]:
    inputs_1 = GI.input if test_string is None else test_string
    
    D : dict[str,Node] = dict()
    for line in inputs_1.strip().splitlines():
        if "->" in line:
            left, right  = line.split("->")
            name, weight = left.strip().split(" ")
            uppers = set(right.strip().split(", "))
        else:
            name, weight = line.split(" ")
            uppers = set()
        weight = int(weight.strip().replace("(","").replace(")",""))

        nodo = Node(name, weight, uppers)
        D[name] = nodo
        
    for name,node in D.items():
        if node.upper:
            for upper_node in node.upper:
                D[upper_node].lower.add(name)

    for name,node in D.items():
        if not node.lower:
            return D, name

    return D, "None"

def get_branch_weight(D: dict[str,Node], name: str) -> int:
    # return weight from the branch starting/including node name
    next_node : list[Node] = [D[name]]
    res = 0
    while next_node:
        nodo = next_node.pop(0)
        res += nodo.weight
        for uppernode in nodo.upper:
            next_node.append(D[uppernode])
        
    return res

def solve_2(D: dict[str,Node], name: str) -> str:
    
    for branch in D[name].upper:
        print(f"from node: {branch} -> {get_branch_weight(D,branch)}")

    return "None"



if __name__ == "__main__":
    test = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""
    D, name = solve_1()
    print(f"Part 1: {name}")
    print(f"Part 2: {solve_2(D, name)}")
