from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


# ---------------------------------------------------------------------------
# Modello del circuito
# ---------------------------------------------------------------------------

@dataclass
class Instruction:
    one: str
    two: str
    operand: str
    dest: str

    def try_eval(self, gates: Dict[str, int]) -> int | None:
        """
        Prova a calcolare il valore del gate:
        - se gli ingressi non sono ancora noti, torna None
        - altrimenti ritorna il valore (0 o 1)
        """
        if self.one not in gates or self.two not in gates:
            return None

        a = gates[self.one]
        b = gates[self.two]

        if self.operand == "AND":
            return a & b
        if self.operand == "OR":
            return a | b
        if self.operand == "XOR":
            return a ^ b

        raise ValueError(f"Operatore sconosciuto: {self.operand}")


def parse_circuit(raw: str) -> tuple[Dict[str, int], List[Instruction]]:
    """
    Parsea l'input in:
      - gates: mappa wire -> valore iniziale (x**, y**, ecc.)
      - instructions: lista di Instruction che definiscono nuovi wire
    """
    gates: Dict[str, int] = {}
    instructions: List[Instruction] = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            # Riga tipo: "x00: 1"
            gate, value_str = line.split(": ")
            gates[gate] = int(value_str)
        elif "->" in line:
            # Riga tipo: "ntg XOR fgs -> mjb"
            left, dest = line.split(" -> ")
            one, operand, two = left.split(" ")
            instructions.append(Instruction(one=one, two=two, operand=operand, dest=dest))

    return gates, instructions


def evaluate_all_gates(
    gates: Dict[str, int],
    instructions: List[Instruction],
) -> Dict[str, int]:
    """
    Risolve tutte le istruzioni finché possibile, propagando i valori.

    Il circuito è combinazionale, quindi non dovrebbero esserci cicli.
    Se rimangono istruzioni impossibili da risolvere, solleva un errore.
    """
    remaining = instructions[:]

    while remaining:
        next_round: List[Instruction] = []
        progress = False

        for instr in remaining:
            res = instr.try_eval(gates)
            if res is None:
                next_round.append(instr)
            else:
                gates[instr.dest] = res
                progress = True

        if not progress:
            # Non si è riusciti a risolvere nessuna nuova istruzione:
            # probabile ciclo o ingresso mancante.
            raise RuntimeError("Impossibile risolvere alcune istruzioni (ciclo o input mancanti).")

        remaining = next_round

    return gates


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> int:
    """
    Calcola il valore numerico rappresentato dai bit z** (z00 = LSB).
    Ritorna un int (l'output richiesto dal puzzle).
    """
    raw = GI.input if test_string is None else test_string

    gates, instructions = parse_circuit(raw)
    evaluate_all_gates(gates, instructions)

    # Raccogliamo tutti i wire che iniziano per 'z'
    z_wires = sorted(name for name in gates.keys() if name.startswith("z"))

    # Nel tuo codice originale:
    #   res = ""
    #   for z in sorted(z_wires):
    #       res = str(gates[z]) + res
    # cioè costruivi la stringa dai bit z00, z01, ... prependendo → MSB..LSB
    # equivalente a iterare z_wires al contrario e fare append.
    bits = "".join(str(gates[z]) for z in reversed(z_wires))
    value = int(bits, 2)

    return value


# ---------------------------------------------------------------------------
# Part 2 – Generazione DOT per Graphviz (output extra)
# ---------------------------------------------------------------------------

def generate_dot(raw: str, filename: str | None = None) -> Path:
    """
    Genera un file .dot per visualizzare il circuito in Graphviz.

    Ritorna il percorso del file .dot generato.
    """
    lines = [ln for ln in raw.splitlines() if ln.strip()]

    # Trova la prima riga con "->" (da lì in poi sono solo le definizioni di gate)
    start_idx = 0
    for i, line in enumerate(lines):
        if "->" in line:
            start_idx = i
            break

    gate_lines = lines[start_idx:]

    dot = []
    dot.append("digraph circuito {")
    dot.append("    rankdir=LR;")
    dot.append('    node [shape=box, style=filled, fillcolor="#CCCCFF"];')

    gate_counter = 0
    wire_nodes: set[str] = set()

    for line in gate_lines:
        left, wire_out = line.split(" -> ")
        wire_a, op, wire_b = left.split()

        gate_name = f"gate{gate_counter}"
        gate_counter += 1

        # Nodo gate (box con label = operatore)
        dot.append(f'    {gate_name} [label="{op}"];')

        # Nodi-wire (ellissi giallognole), definiti una sola volta
        for wire in (wire_a, wire_b, wire_out):
            if wire not in wire_nodes:
                dot.append(
                    f'    {wire} [shape=ellipse, fillcolor="#FFFFCC", style=filled];'
                )
                wire_nodes.add(wire)

        # Connessioni: ingressi → gate → uscita
        dot.append(f"    {wire_a} -> {gate_name};")
        dot.append(f"    {wire_b} -> {gate_name};")
        dot.append(f"    {gate_name} -> {wire_out};")

    dot.append("}")

    dot_text = "\n".join(dot)

    if filename is None:
        # day_24.py -> day_24.dot
        dest = Path(__file__).with_suffix(".dot")
    else:
        dest = Path(__file__).parent / filename

    dest.write_text(dot_text, encoding="utf-8")
    return dest


def solve_2(test_string: str | None = None) -> str:
    """
    Non risolve la Part 2 in automatico (come il tuo codice originale),
    ma genera il file .dot per analizzare il circuito con Graphviz.

    Ritorna il path del file .dot come stringa.
    """
    raw = GI.input if test_string is None else test_string
    dot_path = generate_dot(raw)
    # Commento utile per te: `dot -Tsvg day_24.dot -o day_24.svg`
    return str(dot_path)


# ---------------------------------------------------------------------------
# Main locale
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

    test2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

    print("Test Part 1:", solve_1(test1))
    print("Part 1 (input reale):", solve_1())

    dot_file = solve_2(test2)
    print("DOT di test scritto in:", dot_file)
    print("DOT input reale scritto in:", solve_2())
    # da shell: dot -Tsvg day_24.dot -o day_24.svg
