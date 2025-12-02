from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Set, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()

Coord = Tuple[int, int]
Graph = Dict[Coord, List[Tuple[Coord, int]]]


def _neighbors(grid: List[List[str]], r: int, c: int) -> Iterable[Coord]:
    """Ritorna i vicini raggiungibili rispettando le pendenze."""
    node = grid[r][c]

    if node == ".":
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if grid[nr][nc] != "#":
                yield (nr, nc)
    elif node == "v":
        yield (r + 1, c)
    elif node == "^":
        yield (r - 1, c)
    elif node == ">":
        yield (r, c + 1)
    elif node == "<":
        yield (r, c - 1)


def _num_neighbors(grid: List[List[str]], r: int, c: int) -> int:
    """Numero di vicini raggiungibili (ignorando pendenza) per capire se è un 'nodo'."""
    if grid[r][c] == ".":
        return sum(
            grid[nr][nc] != "#"
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
    # se è una pendenza, ha sempre 1 uscita
    return 1


def _is_node(
    grid: List[List[str]],
    node: Coord,
    source: Coord,
    destination: Coord,
) -> bool:
    """Un 'nodo' è l'origine, la destinazione, o un punto con grado > 2."""
    return node == source or node == destination or _num_neighbors(grid, *node) > 2


def _get_neighbors(
    grid: List[List[str]],
    node: Coord,
    source: Coord,
    destination: Coord,
) -> Iterable[Tuple[Coord, int]]:
    """Da un nodo, cammina finché non trovi il prossimo nodo e ritorna (coord, distanza)."""
    queue: deque[Tuple[Coord, int]] = deque([(node, 0)])
    visited: Set[Coord] = set()

    while queue:
        current, distance = queue.popleft()
        visited.add(current)

        for neighbor in _neighbors(grid, *current):
            if neighbor in visited:
                continue

            if _is_node(grid, neighbor, source, destination):
                yield (neighbor, distance + 1)
            else:
                queue.append((neighbor, distance + 1))


def _graph_from_grid(
    grid: List[List[str]],
    source: Coord,
    destination: Coord,
) -> Graph:
    graph: DefaultDict[Coord, List[Tuple[Coord, int]]] = defaultdict(list)
    queue: deque[Coord] = deque([source])
    visited: Set[Coord] = set()

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in _get_neighbors(grid, node, source, destination):
            graph[node].append((neighbor, weight))
            queue.append(neighbor)

    return dict(graph)


def _parse(data: str) -> Tuple[Graph, Coord, Coord]:
    grid = [list(line) for line in data.splitlines()]
    height, width = len(grid), len(grid[0])

    # blocchiamo ingresso/uscita originari e definiamo source/destination interni
    grid[0][1] = "#"
    grid[height - 1][width - 2] = "#"
    source = (1, 1)
    destination = (height - 2, width - 2)

    graph = _graph_from_grid(grid, source, destination)
    return graph, source, destination


def _parse_no_slopes(data: str) -> Tuple[Graph, Coord, Coord]:
    grid = [
        list(line.replace("^", ".").replace("v", ".").replace("<", ".").replace(">", "."))
        for line in data.splitlines()
    ]
    height, width = len(grid), len(grid[0])

    grid[0][1] = "#"
    grid[height - 1][width - 2] = "#"
    source = (1, 1)
    destination = (height - 2, width - 2)

    graph = _graph_from_grid(grid, source, destination)
    return graph, source, destination


def _longest_path(
    graph: Graph,
    source: Coord,
    destination: Coord,
    distance: int = 0,
    visited: Optional[Set[Coord]] = None,
) -> int:
    """DFS con backtracking per trovare il cammino con distanza massima."""
    if visited is None:
        visited = set()

    if source == destination:
        return distance

    best = 0
    visited.add(source)

    for neighbor, weight in graph.get(source, []):
        if neighbor in visited:
            continue
        best = max(best, _longest_path(graph, neighbor, destination, distance + weight, visited))

    visited.remove(source)
    return best


def solve_1(test_string: str | None = None) -> int:
    """
    Parte 1: pendenze rispettate.
    """
    inputs_1 = GI.input if test_string is None else test_string
    graph, source, destination = _parse(inputs_1)
    # +2 perché nel grafo comprimiamo l'ingresso e l'uscita
    return _longest_path(graph, source, destination) + 2


def solve_2(test_string: str | None = None) -> int:
    """
    Parte 2: pendenze ignorate (trattate come normali '.').
    """
    inputs_1 = GI.input if test_string is None else test_string
    graph, source, destination = _parse_no_slopes(inputs_1)
    return _longest_path(graph, source, destination) + 2


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
