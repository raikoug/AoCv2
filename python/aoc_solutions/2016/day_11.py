from __future__ import annotations

from collections import Counter, deque
from itertools import chain, combinations
from pathlib import Path
from typing import Deque, Iterator, List, Set, Tuple
import re
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Floor = Set[Tuple[str, str]]
Floors = List[Floor]
State = Tuple[int, int, Floors]  # (moves, elevator, floors)


def parse_floors(src: str) -> Floors:
    """Parsa l'input nei piani con (elemento, tipo)."""
    floors: Floors = []
    for line in src.splitlines():
        items = re.findall(r"(\w+)(?:-compatible)? (microchip|generator)", line)
        floors.append(set(items))
    return floors


def is_valid_transition(floor: Floor) -> bool:
    """Un piano è valido se nessun microchip è esposto a generatori estranei."""
    kinds = {kind for _, kind in floor}
    if len(kinds) < 2:
        return True
    # ci sono sia microchip che generatori: ogni microchip deve avere il suo generatore
    return all((obj, "generator") in floor for (obj, kind) in floor if kind == "microchip")


def next_states(state: State) -> Iterator[State]:
    moves, elevator, floors = state
    # possiamo spostare uno o due oggetti dal piano corrente
    possible_moves = chain(
        combinations(floors[elevator], 2),
        combinations(floors[elevator], 1),
    )

    for move in possible_moves:
        for direction in (-1, 1):
            next_elevator = elevator + direction
            if not 0 <= next_elevator < len(floors):
                continue

            next_floors = floors.copy()
            next_floors[elevator] = next_floors[elevator].difference(move)
            next_floors[next_elevator] = next_floors[next_elevator].union(move)

            if is_valid_transition(next_floors[elevator]) and is_valid_transition(next_floors[next_elevator]):
                yield (moves + 1, next_elevator, next_floors)


def is_all_top_level(floors: Floors) -> bool:
    """True se tutti gli oggetti sono sull'ultimo piano."""
    last_index = len(floors) - 1
    return all(not floor for idx, floor in enumerate(floors) if idx < last_index)


def count_floor_objects(state: State) -> Tuple[int, Tuple[Tuple[Tuple[str, int], ...], ...]]:
    """Condensa lo stato in una forma hashabile che ignora le etichette degli elementi.

    Questo sfrutta la simmetria del problema (nomi degli elementi irrilevanti).
    """
    _, elevator, floors = state
    summary = []
    for floor in floors:
        c = Counter(kind for _, kind in floor)
        summary.append(tuple(c.most_common()))
    return elevator, tuple(summary)


def min_moves_to_top_level(floors: Floors) -> int:
    seen: Set[Tuple[int, Tuple[Tuple[Tuple[str, int], ...], ...]]] = set()
    queue: Deque[State] = deque([(0, 0, floors)])

    while queue:
        state = queue.popleft()
        moves, _, floors = state

        if is_all_top_level(floors):
            return moves

        for next_state in next_states(state):
            key = count_floor_objects(next_state)
            if key not in seen:
                seen.add(key)
                queue.append(next_state)

    raise RuntimeError("Nessuna soluzione trovata")


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    floors = parse_floors(raw)
    return min_moves_to_top_level(floors)


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    floors = parse_floors(raw)
    # Aggiungiamo i nuovi oggetti al primo piano
    floors[0] = floors[0].union(
        {
            ("elerium", "generator"),
            ("elerium", "microchip"),
            ("dilithium", "generator"),
            ("dilithium", "microchip"),
        }
    )
    return min_moves_to_top_level(floors)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
