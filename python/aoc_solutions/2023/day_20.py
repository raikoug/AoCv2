from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from math import gcd
from pathlib import Path
from typing import Deque, Dict, List, Literal, Optional, Set, Tuple
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

ModuleType = Literal["broadcaster", "flipflop", "conjunction", "output"]
Pulse = Literal["low", "high"]


@dataclass
class Module:
    name: str
    typ: ModuleType
    outputs: List[str] = field(default_factory=list)
    on: bool = False  # per i flip-flop
    memory: Dict[str, bool] = field(default_factory=dict)  # per le conjunction


def _parse_modules(raw: str) -> Dict[str, Module]:
    modules: Dict[str, Module] = {}

    # Primo passaggio: creo i moduli espliciti
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split("->")
        left = left.strip()
        outputs = [s.strip() for s in right.split(",")]

        if left == "broadcaster":
            name = "broadcaster"
            typ: ModuleType = "broadcaster"
        elif left.startswith("%"):
            name = left[1:]
            typ = "flipflop"
        elif left.startswith("&"):
            name = left[1:]
            typ = "conjunction"
        else:
            raise ValueError(f"Modulo sconosciuto: {left!r}")

        modules[name] = Module(name=name, typ=typ, outputs=outputs)

    # Aggiungo i sink come moduli "output" (così li possiamo referenziare)
    for m in list(modules.values()):
        for out in m.outputs:
            if out not in modules:
                modules[out] = Module(name=out, typ="output", outputs=[])

    # Inizializzo la memoria delle conjunction con tutti gli input a low (False)
    for src in modules.values():
        for dst_name in src.outputs:
            dst = modules[dst_name]
            if dst.typ == "conjunction":
                dst.memory[src.name] = False

    return modules


def _simulate_presses_part1(
    modules: Dict[str, Module],
    presses: int = 1000,
) -> Tuple[int, int]:
    """
    Restituisce (low_count, high_count) dopo `presses` pressioni del bottone.
    """
    low = 0
    high = 0

    for _ in range(presses):
        queue: Deque[Tuple[str, str, bool]] = deque()
        queue.append(("button", "broadcaster", False))  # False = low

        while queue:
            src, dst, is_high = queue.popleft()
            if is_high:
                high += 1
            else:
                low += 1

            if dst not in modules:
                continue

            mod = modules[dst]
            if mod.typ == "output":
                # i sink non propagano ulteriormente
                continue

            if mod.typ == "broadcaster":
                for out in mod.outputs:
                    queue.append((dst, out, is_high))

            elif mod.typ == "flipflop":
                # ignora gli high in ingresso
                if is_high:
                    continue
                mod.on = not mod.on
                out_high = mod.on
                for out in mod.outputs:
                    queue.append((dst, out, out_high))

            elif mod.typ == "conjunction":
                mod.memory[src] = is_high
                # high se NON tutti gli input sono high
                out_high = not all(mod.memory.values())
                for out in mod.outputs:
                    queue.append((dst, out, out_high))

    return low, high


def _lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def _find_rx_press_count(
    modules: Dict[str, Module],
    rx_name: str = "rx",
    max_presses: int = 10_000_000,
) -> int:
    """
    Trova il numero minimo di pressioni del bottone affinché `rx` riceva
    un impulso low.

    Per l'input di AoC 2023 day 20, `rx` è collegato ad una conjunction
    (chiamiamola RX_IN). RX_IN manda low verso rx quando TUTTI i suoi
    ingressi sono high. Ogni ingresso ha un periodo diverso.

    Strategia:
    - Trova RX_IN (modulo che ha `rx` tra le outputs).
    - Trova tutti i moduli che hanno RX_IN tra le outputs (i "genitori").
    - Per ogni genitore, misura il periodo con cui manda HIGH verso RX_IN
      (distanza tra due high consecutivi).
    - Restituisce l'MCM di tutti questi periodi.
    """
    # Trovo il modulo che alimenta rx
    rx_input: Optional[str] = None
    for m in modules.values():
        if rx_name in m.outputs:
            rx_input = m.name
            break

    if rx_input is None:
        raise ValueError("Nessun modulo che alimenta 'rx' trovato.")

    # Moduli che alimentano direttamente rx_input
    inputs_to_rx_input: Set[str] = {
        m.name for m in modules.values() if rx_input in m.outputs
    }

    # Per ogni input, memorizzo le prime due pressioni in cui manda HIGH a rx_input
    high_events: Dict[str, List[int]] = {name: [] for name in inputs_to_rx_input}

    press = 0
    while press < max_presses:
        press += 1
        queue: Deque[Tuple[str, str, bool]] = deque()
        queue.append(("button", "broadcaster", False))  # False = low

        while queue:
            src, dst, is_high = queue.popleft()

            if dst not in modules:
                continue

            mod = modules[dst]
            if mod.typ == "output":
                continue

            # Se questo è un HIGH verso rx_input da uno dei suoi genitori, lo registro
            if dst == rx_input and src in inputs_to_rx_input and is_high:
                events = high_events[src]
                # salvo solo se non abbiamo già 2 eventi
                if len(events) < 2:
                    events.append(press)

            if mod.typ == "broadcaster":
                for out in mod.outputs:
                    queue.append((dst, out, is_high))

            elif mod.typ == "flipflop":
                if is_high:
                    continue
                mod.on = not mod.on
                out_high = mod.on
                for out in mod.outputs:
                    queue.append((dst, out, out_high))

            elif mod.typ == "conjunction":
                mod.memory[src] = is_high
                out_high = not all(mod.memory.values())
                for out in mod.outputs:
                    queue.append((dst, out, out_high))

        # Se per tutti gli input abbiamo almeno due high, possiamo calcolare i periodi
        if all(len(ev) >= 2 for ev in high_events.values()):
            break

    if not all(len(ev) >= 2 for ev in high_events.values()):
        raise RuntimeError("Non ho osservato due HIGH per tutti i rami entro max_presses.")

    # Periodo per ciascun ramo = differenza tra i primi due eventi HIGH
    periods = [ev[1] - ev[0] for ev in high_events.values()]

    # LCM di tutti i periodi
    result = 1
    for p in periods:
        result = _lcm(result, p)
    return result


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    modules = _parse_modules(raw)
    low, high = _simulate_presses_part1(modules, presses=1000)
    return low * high


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    modules = _parse_modules(raw)
    return _find_rx_press_count(modules)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
