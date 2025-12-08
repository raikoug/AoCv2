from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput

from typing import TypeAlias, Callable
from dataclasses import dataclass
from math import sqrt, prod

GI = GetInput()

JuncBox: TypeAlias = tuple[int, int, int]

# Per l'ordinamento basterebbe anche la distanza al quadrato,
# ma teniamo la tua definizione per chiarezza.
distance: Callable[[JuncBox, JuncBox], float] = (
    lambda a, b: sqrt(
        (b[0] - a[0]) ** 2
        + (b[1] - a[1]) ** 2
        + (b[2] - a[2]) ** 2
    )
)


@dataclass
class Connection:
    node1: JuncBox
    node2: JuncBox

    def __eq__(self, other) -> bool:
        if not isinstance(other, Connection):
            return False

        # Connessione non orientata: (A,B) == (B,A)
        if self.node1 == other.node1 and self.node2 == other.node2:
            return True
        if self.node1 == other.node2 and self.node2 == other.node1:
            return True

        return False


class DisjointSet:
    """
    Union-Find / Disjoint Set per tenere traccia dei circuiti.
    Ogni JuncBox parte come proprio gruppo, poi i gruppi
    vengono uniti a mano a mano che aggiungiamo connessioni.
    """

    def __init__(self, nodes: list[JuncBox]) -> None:
        # parent[x] = rappresentante del gruppo di x
        self.parent: dict[JuncBox, JuncBox] = {n: n for n in nodes}
        # size[root] = numero di elementi nel gruppo con radice root
        self.size: dict[JuncBox, int] = {n: 1 for n in nodes}

    def find(self, x: JuncBox) -> JuncBox:
        """Trova la radice del gruppo di x (con path compression)."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: JuncBox, b: JuncBox) -> bool:
        """
        Unisce i gruppi che contengono a e b.
        Ritorna True se avviene una fusione reale (due gruppi distinti),
        False se erano già nello stesso gruppo (caso 'nothing happens').
        """
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            # Già nello stesso circuito
            return False

        # Union by size: attach più piccolo al più grande
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def component_sizes(self) -> list[int]:
        """
        Restituisce la lista delle dimensioni di tutti i gruppi (circuiti).
        """
        root_counts: dict[JuncBox, int] = {}
        for node in self.parent.keys():
            root = self.find(node)
            root_counts[root] = root_counts.get(root, 0) + 1
        return list(root_counts.values())


class Circuits:
    """
    Wrapper 'ad alto livello' sui circuiti:
    - inizializza un gruppo per ogni JuncBox
    - applica le Connection
    - calcola le dimensioni dei circuiti.
    """

    def __init__(self, boxes: list[JuncBox]) -> None:
        self._dsu = DisjointSet(boxes)

    def connect(self, conn: Connection) -> None:
        """
        Applica una connessione tra due junction box.
        Anche se la connessione è 'ridondante' (stesso gruppo),
        fa comunque parte del processo (una delle N coppie).
        """
        self._dsu.union(conn.node1, conn.node2)

    def component_sizes(self) -> list[int]:
        return self._dsu.component_sizes()


def solve_1(test_string: str | None = None) -> int:
    # Numero di coppie da considerare:
    # - 10 per l'esempio (come nel testo)
    # - 1000 per l'input reale del puzzle
    if test_string is None:
        inputs_1 = GI.input
        couples = 1000
    else:
        inputs_1 = test_string
        couples = 10

    # Parsing delle coordinate
    juncboxes: list[JuncBox] = []
    for line in inputs_1.strip().splitlines():
        x_str, y_str, z_str = line.split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        juncboxes.append((x, y, z))

    # Calcolo di tutte le distanze tra coppie (non orientate, una sola volta)
    distances: list[tuple[float, JuncBox, JuncBox]] = []
    juc_quantity = len(juncboxes)

    for j in range(juc_quantity):
        node1 = juncboxes[j]
        for k in range(j + 1, juc_quantity):
            node2 = juncboxes[k]
            distances.append((distance(node1, node2), node1, node2))

    # Ordiniamo per distanza crescente
    distances.sort(key=lambda a: a[0])

    # Prendiamo solo le prime `couples` coppie.
    couples = min(couples, len(distances))
    connections: list[Connection] = [
        Connection(node1=d[1], node2=d[2])
        for d in distances[:couples]
    ]

    # Costruiamo i circuiti applicando le connessioni
    circuits = Circuits(juncboxes)
    for conn in connections:
        circuits.connect(conn)

    # Dimensioni dei circuiti (componenti connesse)
    sizes = circuits.component_sizes()
    sizes.sort(reverse=True)

    # Prendiamo le 3 più grandi e facciamo il prodotto
    top3 = sizes[:3]
    answer = prod(top3)

    return answer


def solve_2(test_string: str | None = None)  -> int:
    if test_string is None:
        inputs_1 = GI.input
    else:
        inputs_1 = test_string

    juncboxes: list[JuncBox] = []
    for line in inputs_1.strip().splitlines():
        x_str, y_str, z_str = line.split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        juncboxes.append((x, y, z))

    distances: list[tuple[float, JuncBox, JuncBox]] = []
    juc_quantity = len(juncboxes)

    for j in range(juc_quantity):
        node1 = juncboxes[j]
        for k in range(j + 1, juc_quantity):
            node2 = juncboxes[k]
            distances.append((distance(node1, node2), node1, node2))

    distances.sort(key=lambda a: a[0])
    connections: list[Connection] = list()
    sizes: int = len(distances)
    d = distances[0]

    # Prendiamo solo le prime `couples` coppie.
    while sizes != 1:
        d = distances.pop(0)
        connections.append(Connection(node1=d[1], node2=d[2]))

        circuits = Circuits(juncboxes)
        for conn in connections:
            circuits.connect(conn)

        sizes = len(circuits.component_sizes())

    return d[1][0] * d[2][0]


if __name__ == "__main__":
    test = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
