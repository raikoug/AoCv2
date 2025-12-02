from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional, List, Set, Tuple, Dict

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


def _parse_card(line: str) -> Tuple[int, Set[int], List[int]]:
    """Parsa una riga del tipo:
    "Card   1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    Restituisce (card_id, winning_numbers, numbers).
    """
    prefix, rest = line.split(":", 1)
    card_id = int(prefix.strip().split()[1])
    left, right = rest.split("|", 1)
    winning = {int(x) for x in left.strip().split() if x}
    numbers = [int(x) for x in right.strip().split() if x]
    return card_id, winning, numbers


def solve_1(test_string: Optional[str] = None) -> int:
    """Calcola il punteggio totale delle scratchcards (regola 2^(matches-1))."""
    raw = GI.input if test_string is None else test_string
    total = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        _, winning, numbers = _parse_card(line)
        matches = len(winning.intersection(numbers))
        if matches > 0:
            total += 2 ** (matches - 1)

    return total


def solve_2(test_string: Optional[str] = None) -> int:
    """Calcola il numero totale di carte tenendo conto dei 'cloni'."""
    raw = GI.input if test_string is None else test_string
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    cards: List[Tuple[int, Set[int], List[int]]] = [
        _parse_card(line) for line in lines
    ]
    # Manteniamo l'ordine per ID crescente
    cards.sort(key=lambda x: x[0])

    copies: Dict[int, int] = {card_id: 1 for card_id, _, _ in cards}

    for card_id, winning, numbers in cards:
        count = copies[card_id]
        matches = len(winning.intersection(numbers))
        for offset in range(1, matches + 1):
            next_id = card_id + offset
            if next_id in copies:
                copies[next_id] += count

    return sum(copies.values())


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
