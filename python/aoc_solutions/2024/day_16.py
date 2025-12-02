from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set, Tuple

import heapq
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Pos = Tuple[int, int]  # (row, col)
Dir = Tuple[int, int]  # (dr, dc)
State = Tuple[Pos, Dir]
GridMap = Dict[Pos, str]

DIRS: Tuple[Dir, ...] = (
    (1, 0),   # down
    (0, 1),   # right
    (-1, 0),  # up
    (0, -1),  # left
)

INF = 10**18


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_grid(raw: str) -> Tuple[GridMap, Pos, Pos]:
    """
    Parla la griglia in un dict {(row, col): char}, e trova S ed E.
    """
    lines = raw.splitlines()
    grid: GridMap = {}
    start: Pos | None = None
    end: Pos | None = None

    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            grid[(r, c)] = ch
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)

    if start is None or end is None:
        raise ValueError("Start 'S' o End 'E' non trovati nella griglia.")

    return grid, start, end


# ---------------------------------------------------------------------------
# Dijkstra + ricostruzione dei percorsi minimi
# ---------------------------------------------------------------------------

def dijkstra_all_best_paths(grid: GridMap, start: Pos, end: Pos) -> Tuple[int, Set[Pos]]:
    """
    Esegue Dijkstra sugli stati (posizione, direzione):

      - costo 1 per avanzare nella stessa direzione
      - costo 1000 per girare + 1 per avanzare -> 1001 se cambia direzione

    Restituisce:
      - best_cost: costo minimo per raggiungere la cella end
      - best_tiles: insieme di tutte le posizioni (row, col) che appartengono
        ad almeno un percorso di costo minimo.
    """
    # direzione iniziale: verso destra (0, 1) come nell'originale
    start_dir: Dir = (0, 1)
    start_state: State = (start, start_dir)

    dist: Dict[State, int] = {start_state: 0}
    parents: Dict[State, Set[State]] = {}

    heap: List[Tuple[int, State]] = [(0, start_state)]

    while heap:
        score, state = heapq.heappop(heap)
        pos, face = state

        # entry obsoleta?
        if score != dist.get(state, INF):
            continue

        # esplora vicini
        for d in DIRS:
            nr, nc = pos[0] + d[0], pos[1] + d[1]
            npos: Pos = (nr, nc)

            if grid.get(npos, "#") == "#":
                continue

            step_cost = 1 if d == face else 1001
            new_score = score + step_cost
            nstate: State = (npos, d)

            old_dist = dist.get(nstate, INF)
            if new_score < old_dist:
                dist[nstate] = new_score
                parents[nstate] = {state}
                heapq.heappush(heap, (new_score, nstate))
            elif new_score == old_dist:
                # nuovo padre per un percorso alternativo, stesso costo minimo
                parents.setdefault(nstate, set()).add(state)

    # Troviamo tutti gli stati di arrivo in end con costo minimo
    goal_states: List[State] = []
    best_cost = INF
    for st, sc in dist.items():
        pos, _ = st
        if pos == end:
            if sc < best_cost:
                best_cost = sc
                goal_states = [st]
            elif sc == best_cost:
                goal_states.append(st)

    if best_cost == INF or not goal_states:
        raise ValueError("Nessun percorso dalla S alla E.")

    # Risaliamo tutti i percorsi minimi all'indietro per ottenere le piastrelle
    best_tiles: Set[Pos] = set()
    stack: List[State] = list(goal_states)
    seen_states: Set[State] = set()

    while stack:
        st = stack.pop()
        if st in seen_states:
            continue
        seen_states.add(st)

        pos, _ = st
        best_tiles.add(pos)

        for parent in parents.get(st, []):
            stack.append(parent)

    return best_cost, best_tiles


# ---------------------------------------------------------------------------
# Solve 1 & 2
# ---------------------------------------------------------------------------

def _solve(raw: str) -> Tuple[int, int]:
    grid, start, end = parse_grid(raw)
    best_cost, best_tiles = dijkstra_all_best_paths(grid, start, end)
    return best_cost, len(best_tiles)


def solve_1(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    part1, _ = _solve(inputs_1)
    return part1


def solve_2(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string
    _, part2 = _solve(inputs_1)
    return part2


if __name__ == "__main__":
    test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    test_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

    p1, p2 = _solve(test)
    print(f"Test Part 1: {p1}")
    print(f"Test Part 2: {p2}")

    print(f"Part 1 (input reale): {solve_1()}")
    print(f"Part 2 (input reale): {solve_2()}")
