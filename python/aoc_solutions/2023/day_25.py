from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

import sys

import networkx as nx  # type: ignore[import-untyped]

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def _parse_graph(data: str) -> nx.Graph:
    """
    Ogni riga: 'aaa: bbb ccc ddd'
    """
    G = nx.Graph()
    for line in data.splitlines():
        if not line.strip():
            continue
        left, right = line.split(":")
        src = left.strip()
        neighbors = [n.strip() for n in right.strip().split()]
        for dst in neighbors:
            G.add_edge(src, dst)
    return G


def _min_cut_product(G: nx.Graph) -> int:
    """
    Trova il minimum edge cut, rimuove quegli archi e moltiplica
    le dimensioni dei due componenti risultanti.
    """
    # Trova il cut minimo (per AoC 2023 è di grandezza 3)
    min_cut_edges = nx.minimum_edge_cut(G)

    G_copy = G.copy()
    G_copy.remove_edges_from(min_cut_edges)

    components = list(nx.connected_components(G_copy))
    if len(components) != 2:
        raise ValueError(f"Attesi 2 componenti dopo il cut, trovati {len(components)}")

    size1 = len(components[0])
    size2 = len(components[1])
    return size1 * size2


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    G = _parse_graph(inputs_1)
    return _min_cut_product(G)


def solve_2(test_string: str | None = None) -> int:
    """
    Day 25 ha solo una parte; qui ritorno 0 come placeholder.
    Se un giorno AoC aggiunge una part 2, questa è pronta da riempire.
    """
    _ = GI.input if test_string is None else test_string
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
