from __future__ import annotations

from pathlib import Path
from typing import Dict, Set, Tuple, List

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Graph = Dict[str, Set[str]]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_graph(raw: str) -> Graph:
    """
    Input tipo:

        aa-bb
        bb-cc
        ...

    Restituisce un grafo non orientato: node -> insieme di vicini.
    """
    graph: Graph = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = line.split("-")
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


# ---------------------------------------------------------------------------
# Part 1 – Triangoli con almeno un computer 't*'
# ---------------------------------------------------------------------------

def count_triangles_with_t(graph: Graph) -> int:
    """
    Conta il numero di triple (A,B,C) tali che:
      - A, B, C sono tutte connesse fra loro (triangolo / 3-clique),
      - almeno uno dei tre nomi inizia con 't'.

    Ogni triangolo è contato una sola volta.
    """
    triangles = 0
    nodes = sorted(graph.keys())

    # imponiamo un ordine lessicografico A < B < C per evitare duplicati
    for i, a in enumerate(nodes):
        neighbors_a = graph[a]
        for b in neighbors_a:
            if b <= a:
                continue  # assicuriamo A < B
            neighbors_b = graph[b]
            # C deve essere vicino sia ad A che a B
            common = neighbors_a & neighbors_b
            for c in common:
                if c <= b:
                    continue  # A < B < C
                if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                    triangles += 1

    return triangles


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    graph = parse_graph(raw)
    return count_triangles_with_t(graph)


# ---------------------------------------------------------------------------
# Part 2 – Massima clique (LAN party più grande)
# ---------------------------------------------------------------------------

def bron_kerbosch(
    R: Set[str],
    P: Set[str],
    X: Set[str],
    graph: Graph,
    best: List[Set[str]],
) -> None:
    """
    Algoritmo Bron–Kerbosch con pivot per trovare la clique massima.
    - R: insieme corrente nella clique
    - P: candidati da aggiungere
    - X: vertici già esplorati
    - best[0]: clique migliore trovata finora
    """
    # se non ci sono più candidati né esclusi, R è una clique massimale
    if not P and not X:
        if len(R) > len(best[0]):
            best[0] = set(R)
        return

    # pruning: anche se aggiungessi tutti i candidati, non supererei best
    if len(R) + len(P) <= len(best[0]):
        return

    # pivot: prendiamo un vertice con molti vicini per ridurre i rami
    # (P ∪ X) può essere vuoto se siamo vicini alla foglia
    union = P | X
    if union:
        u = max(union, key=lambda v: len(graph[v]))
        candidates = P - graph[u]
    else:
        candidates = set(P)

    for v in list(candidates):
        neighbors_v = graph[v]
        bron_kerbosch(
            R | {v},
            P & neighbors_v,
            X & neighbors_v,
            graph,
            best,
        )
        P.remove(v)
        X.add(v)


def largest_clique(graph: Graph) -> Set[str]:
    """
    Restituisce l'insieme di nodi appartenenti alla clique massima.
    """
    all_nodes = set(graph.keys())
    best: List[Set[str]] = [set()]
    bron_kerbosch(set(), set(all_nodes), set(), graph, best)
    return best[0]


def solve_2(test_string: str | None = None) -> str:
    raw = GI.input if test_string is None else test_string
    graph = parse_graph(raw)
    clique = largest_clique(graph)
    return ",".join(sorted(clique))


# ---------------------------------------------------------------------------
# Test manuale
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    print(f"Part 1 (test): {solve_1(test)}")
    print(f"Part 2 (test): {solve_2(test)}")

    print(f"Part 1 (input reale): {solve_1()}")
    print(f"Part 2 (input reale): {solve_2()}")
