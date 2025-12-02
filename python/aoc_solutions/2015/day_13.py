from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


@dataclass
class Person:
    """Mappa il nome di una persona alla felicità verso ogni vicino."""

    name: str
    happiness_to: Dict[str, int]

    @classmethod
    def from_lines(cls, lines: List[str]) -> "Person":
        name = lines[0].split()[0]
        happiness_to: Dict[str, int] = {}
        for line in lines:
            # Alice would gain 2 happiness units by sitting next to Bob.
            tokens = line.split()
            src = tokens[0]
            sign = 1 if tokens[2] == "gain" else -1
            amount = int(tokens[3]) * sign
            dest = tokens[-1].rstrip(".")
            happiness_to[dest] = amount
        return cls(name=name, happiness_to=happiness_to)


@dataclass
class Table:
    persons: Dict[str, Person]
    people: Set[str]

    @classmethod
    def from_string(cls, s: str, include_me: bool = False) -> "Table":
        people: Set[str] = {line.split()[0] for line in s.splitlines() if line}
        lines = s.splitlines()

        if include_me:
            # Aggiungiamo "Me" con 0 verso tutti e viceversa
            for person in list(people):
                lines.append(f"Me would gain 0 happiness units by sitting next to {person}.")
                lines.append(f"{person} would gain 0 happiness units by sitting next to Me.")
            people.add("Me")

        persons: Dict[str, Person] = {}
        for person in people:
            person_lines = [line for line in lines if line.startswith(person + " ")]
            persons[person] = Person.from_lines(person_lines)

        return cls(persons=persons, people=people)

    def calc_happiness(self, seating: Sequence[str]) -> int:
        """Calcola la felicità totale per una disposizione circolare."""
        total = 0
        n = len(seating)
        for i, person in enumerate(seating):
            left = seating[(i - 1) % n]
            right = seating[(i + 1) % n]
            total += self.persons[person].happiness_to[left]
            total += self.persons[person].happiness_to[right]
        return total


def _max_happiness(table: Table) -> int:
    """Calcola la massima felicità possibile fissando una persona per rompere la simmetria circolare."""
    people = sorted(table.people)
    first = people[0]
    others = [p for p in people if p != first]

    best = -10**9
    for perm in permutations(others):
        seating = (first,) + perm
        score = table.calc_happiness(seating)
        if score > best:
            best = score
    return best


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    # Le linee terminano con '.', che non serve per il parsing
    cleaned = raw.replace(".", "")
    table = Table.from_string(cleaned, include_me=False)
    return _max_happiness(table)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    cleaned = raw.replace(".", "")
    table = Table.from_string(cleaned, include_me=True)
    return _max_happiness(table)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
