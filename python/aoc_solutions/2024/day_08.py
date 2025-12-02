from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path
from typing import Dict, Iterator

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


# --- Modello dati ---------------------------------------------------------


@dataclass(frozen=True)
class Node:
    row: int
    col: int

    def __str__(self) -> str:
        return f"row: {self.row}, col: {self.col}"


class Antenna(list[Node]):
    """
    Una singola "famiglia" di antenne dello stesso tipo (stesso carattere).
    Mantiene:
    - i nodi antenna (inherited list[Node])
    - l'insieme degli antinodi generati
    - dimensioni massime della griglia
    - modalità v1/v2 (v2 = con tutte le armoniche lungo la retta)
    """

    def __init__(
        self,
        a_type: str,
        max_row: int,
        max_col: int,
        v2: bool = False,
    ) -> None:
        super().__init__()
        self.a_type: str = a_type
        self.antinodes: set[Node] = set()
        self.max_row: int = max_row
        self.max_col: int = max_col
        self.v2: bool = v2

    # --- Utilità di validazione ------------------------------------------

    def is_valid_node(self, node: Node) -> bool:
        return (
            0 <= node.row <= self.max_row
            and 0 <= node.col <= self.max_col
        )

    # --- Logica per gli antinodi -----------------------------------------

    def add_antinodes(self, one: Node, two: Node) -> None:
        """
        Aggiunge antinodi generati dalla coppia (one, two).
        - v1: solo i due punti simmetrici.
        - v2: tutti i punti sulla retta (in entrambe le direzioni) finché restano in griglia.
        """
        if not self.v2:
            # Versione parte 1: due soli antinodi simmetrici
            antinode1 = Node(2 * one.row - two.row, 2 * one.col - two.col)
            antinode2 = Node(2 * two.row - one.row, 2 * two.col - one.col)

            if self.is_valid_node(antinode1):
                self.antinodes.add(antinode1)

            if self.is_valid_node(antinode2):
                self.antinodes.add(antinode2)
        else:
            # Versione parte 2: tutte le armoniche lungo la retta
            dr = two.row - one.row
            dc = two.col - one.col
            g = gcd(abs(dr), abs(dc))
            ur = dr // g  # unit row step
            uc = dc // g  # unit col step

            # In avanti (n >= 0)
            n = 0
            while True:
                row = one.row + n * ur
                col = one.col + n * uc
                antinode = Node(row, col)
                if self.is_valid_node(antinode):
                    self.antinodes.add(antinode)
                    n += 1
                else:
                    break

            # All'indietro (n < 0)
            n = -1
            while True:
                row = one.row + n * ur
                col = one.col + n * uc
                antinode = Node(row, col)
                if self.is_valid_node(antinode):
                    self.antinodes.add(antinode)
                    n -= 1
                else:
                    break

    # --- Gestione antenne di questo tipo ---------------------------------

    def post_append(self, node: Node) -> None:
        """
        Dopo aver aggiunto una nuova antenna di questo tipo, genera gli antinodi
        con tutte le antenne precedenti della stessa famiglia.
        """
        if len(self) <= 1:
            return

        for other in self[:-1]:
            self.add_antinodes(node, other)

    def add_antenna(self, node: Node) -> None:
        self.append(node)
        self.post_append(node)

    def __str__(self) -> str:  # solo per debug eventuale
        return f"Nodes: {list(self)}, type: {self.a_type}, antinodes: {self.antinodes}"


class Antennas(Dict[str, Antenna]):
    """
    Collezione di antenne indicizzate per carattere (tipo).
    Tiene anche:
    - max_row / max_col della griglia
    - flag v2 per controllare il comportamento degli antinodi
    """

    def __init__(self, max_row: int = 0, max_col: int = 0, v2: bool = False) -> None:
        super().__init__()
        self.max_row: int = max_row
        self.max_col: int = max_col
        self.v2: bool = v2

    def _new_antenna(self, antenna_type: str, node: Node) -> None:
        self[antenna_type] = Antenna(
            a_type=antenna_type,
            max_row=self.max_row,
            max_col=self.max_col,
            v2=self.v2,
        )
        self._update_antenna(antenna_type, node)

    def _update_antenna(self, antenna_type: str, node: Node) -> None:
        self[antenna_type].add_antenna(node)

    def add(self, antenna_type: str, row: int, col: int) -> None:
        node = Node(row, col)
        if antenna_type in self:
            self._update_antenna(antenna_type, node)
        else:
            self._new_antenna(antenna_type, node)


# --- Logica comune per solve_1 / solve_2 ---------------------------------


def _count_antinodes(inputs: str, use_v2: bool) -> int:
    rows = inputs.splitlines()
    if not rows:    
    return 0

    max_row = len(rows) - 1
    max_col = len(rows[0]) - 1

    antennas = Antennas(max_row=max_row, max_col=max_col, v2=use_v2)

    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch != ".":
                antennas.add(ch, r, c)

    # Raccogli tutti gli antinodi da tutte le antenne
    all_antinodes: set[Node] = set()
    for antenna in antennas.values():
        all_antinodes.update(antenna.antinodes)

    return len(all_antinodes)


# --- API richieste dal template ------------------------------------------


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    return _count_antinodes(inputs_1, use_v2=False)


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    return _count_antinodes(inputs_1, use_v2=True)


if __name__ == "__main__":
    test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    # Input reale da Advent of Code
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")

    # Per test locale:
    # print(f"Part 1 (test): {solve_1(test)}")
    # print(f"Part 2 (test): {solve_2(test)}")
