from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import sys
from collections import Counter

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

CARD_ORDER_PART1 = "23456789TJQKA"
CARD_ORDER_PART2 = "J23456789TQKA"

CARD_VALUE_P1: Dict[str, int] = {c: i for i, c in enumerate(CARD_ORDER_PART1)}
CARD_VALUE_P2: Dict[str, int] = {c: i for i, c in enumerate(CARD_ORDER_PART2)}


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int


def _hand_type(cards: str, use_jokers: bool) -> int:
    """
    Valuta la forza della mano restituendo un intero 1..7:
    1: High card
    2: One pair
    3: Two pair
    4: Three of a kind
    5: Full house
    6: Four of a kind
    7: Five of a kind
    Con use_jokers=True, le 'J' diventano jolly.
    """
    counts = Counter(cards)
    if use_jokers:
        jokers = counts.pop("J", 0)
        if jokers == 5:
            return 7  # tutti jolly -> five of a kind
        if counts:
            # Aggiungi tutti i jolly al gruppo più numeroso
            max_rank = max(counts, key=lambda c: counts[c])
            counts[max_rank] += jokers

    groups = sorted(counts.values(), reverse=True)
    if groups[0] == 5:
        return 7
    if groups[0] == 4:
        return 6
    if groups[0] == 3 and len(groups) > 1 and groups[1] == 2:
        return 5
    if groups[0] == 3:
        return 4
    if groups[0] == 2 and len(groups) > 1 and groups[1] == 2:
        return 3
    if groups[0] == 2:
        return 2
    return 1


def _sort_key(hand: Hand, use_jokers: bool) -> Tuple[int, List[int]]:
    mapping = CARD_VALUE_P2 if use_jokers else CARD_VALUE_P1
    t = _hand_type(hand.cards, use_jokers)
    ranks = [mapping[c] for c in hand.cards]
    return t, ranks


def _parse_hands(raw: str) -> List[Hand]:
    hands: List[Hand] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        cards, bid_str = line.split()
        hands.append(Hand(cards=cards, bid=int(bid_str)))
    return hands


def _total_winnings(raw: str, use_jokers: bool) -> int:
    hands = _parse_hands(raw)
    # Ordiniamo dalla mano più debole alla più forte
    hands.sort(key=lambda h: _sort_key(h, use_jokers))
    total = 0
    for rank, hand in enumerate(hands, start=1):
        total += hand.bid * rank
    return total


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    return _total_winnings(raw, use_jokers=False)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    return _total_winnings(raw, use_jokers=True)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
