from __future__ import annotations

from pathlib import Path
from typing import Optional, Set, Tuple, List
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Pos = Tuple[int, int]
DELTAS: Tuple[Pos, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _parse_grid(raw: str) -> Tuple[List[str], Pos]:
    lines = [line for line in raw.splitlines() if line.strip()]
    start: Optional[Pos] = None
    for r, row in enumerate(lines):
        c = row.find("S")
        if c != -1:
            start = (r, c)
            break
    if start is None:
        raise ValueError("Nessuna 'S' trovata nella griglia.")
    return lines, start


def _reachable_after_steps(
    grid: List[str],
    start: Pos,
    steps: int,
    infinite: bool = False,
) -> int:
    """
    BFS per "frontiere": posizioni raggiungibili esattamente dopo `steps`
    passi. Se infinite=True, la griglia viene tilata all'infinito usando
    modulo (classico AoC 2023 day 21).
    """
    rows = len(grid)
    cols = len(grid[0])
    frontier: Set[Pos] = {start}

    for _ in range(steps):
        new_frontier: Set[Pos] = set()
        for (r, c) in frontier:
            for dr, dc in DELTAS:
                nr, nc = r + dr, c + dc
                if infinite:
                    rr = nr % rows
                    cc = nc % cols
                    if grid[rr][cc] != "#":
                        new_frontier.add((nr, nc))
                else:
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                        new_frontier.add((nr, nc))
        frontier = new_frontier

    return len(frontier)


def _count_infinite_big(
    grid: List[str],
    start: Pos,
    steps: int,
) -> int:
    """
    Usa l'osservazione classica: per AoC 2023 day 21, il numero di plot
    raggiungibili come funzione del numero di tile "lontani" è un polinomio
    quadratico. Calcoliamo tre punti equispaziati e interpoliamo.
    """
    rows = len(grid)
    base = steps % rows

    if steps < 3 * rows:
        # per passi piccoli, non ha senso fare l'extrapolazione
        return _reachable_after_steps(grid, start, steps, infinite=True)

    f0 = _reachable_after_steps(grid, start, base, infinite=True)
    f1 = _reachable_after_steps(grid, start, base + rows, infinite=True)
    f2 = _reachable_after_steps(grid, start, base + 2 * rows, infinite=True)

    # f(n) = A n^2 + B n + C, con n = 0,1,2 corrispondenti a f0,f1,f2
    a_val = f0
    b_val = f1
    c_val = f2

    diff1 = b_val - a_val
    diff2 = c_val - b_val
    diff3 = diff2 - diff1

    A = diff3 // 2
    B = diff1 - 3 * A
    C = a_val - A - B

    n = (steps - base) // rows
    return A * n * n + B * n + C


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid, start = _parse_grid(raw)

    # Per AoC 2023 day 21: 64 passi. Se ci passi una stringa di test,
    # puoi cambiare qui se vuoi testare un'altra distanza.
    steps = 6 if test_string is not None else 64
    return _reachable_after_steps(grid, start, steps, infinite=False)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    grid, start = _parse_grid(raw)

    # Distanza "gigante" ufficiale del problema
    steps = 26501365
    return _count_infinite_big(grid, start, steps)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
