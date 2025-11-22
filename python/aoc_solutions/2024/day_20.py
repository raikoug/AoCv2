from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import List, Tuple

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)

Grid = List[List[str]]
Pos = Tuple[int, int]  # (row, col)

DIRS: tuple[Pos, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_grid(raw: str) -> tuple[Grid, Pos, Pos]:
    grid: Grid = [list(r) for r in raw.splitlines() if r.strip()]
    H, W = len(grid), len(grid[0])
    start: Pos | None = None
    end: Pos | None = None

    for r in range(H):
        for c in range(W):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    if start is None or end is None:
        raise ValueError("Start 'S' o End 'E' non trovati nella griglia.")

    return grid, start, end


def in_bounds(r: int, c: int, H: int, W: int) -> bool:
    return 0 <= r < H and 0 <= c < W


def bfs_no_cheat(grid: Grid, start: Pos) -> List[List[int]]:
    """
    BFS classico che ignora i muri ('#') e calcola la distanza minima
    da `start` a ogni cella:
      - dist[r][c] = numero minimo di passi, oppure -1 se irraggiungibile.
    """
    H, W = len(grid), len(grid[0])
    dist = [[-1] * W for _ in range(H)]
    sr, sc = start
    dist[sr][sc] = 0
    q: deque[Pos] = deque([start])

    while q:
        r, c = q.popleft()
        d = dist[r][c]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, H, W) and grid[nr][nc] != "#" and dist[nr][nc] < 0:
                dist[nr][nc] = d + 1
                q.append((nr, nc))

    return dist


# ---------------------------------------------------------------------------
# Parte 1 – cheat di esattamente 2 passi
# ---------------------------------------------------------------------------

def solve_1(test_string: str | None = None) -> int:
    """
    Conta quanti cheat (segmenti di 2 passi ignorando muri) permettono
    di risparmiare almeno:
      - 20 picosecondi sul sample
      - 100 picosecondi sull'input reale
    rispetto al percorso base.
    """
    raw = GI.input if test_string is None else test_string
    grid, start, end = parse_grid(raw)
    H, W = len(grid), len(grid[0])

    # Distanze senza cheat
    dist_from_start = bfs_no_cheat(grid, start)
    dist_from_end = bfs_no_cheat(grid, end)
    base_dist = dist_from_start[end[0]][end[1]]
    if base_dist < 0:
        return 0  # nessun percorso

    saving_threshold = 20 if test_string is not None else 100
    cheat_length = 2

    count = 0

    for r in range(H):
        for c in range(W):
            if dist_from_start[r][c] < 0:
                continue  # non raggiungibile senza cheat

            dist_here = dist_from_start[r][c]

            # Consideriamo tutte le celle a distanza di grafo 2 (ignorando muri),
            # cioè con |dr| + |dc| <= 2. Il costo del cheat è *sempre* 2.
            for dr in range(-2, 3):
                rem = 2 - abs(dr)
                for dc in range(-rem, rem + 1):
                    if dr == 0 and dc == 0:
                        continue  # cheat di zero passi non ha senso
                    nr, nc = r + dr, c + dc
                    if not in_bounds(nr, nc, H, W):
                        continue
                    if dist_from_end[nr][nc] < 0:
                        continue  # da qui non arrivo a 'E' in modo normale

                    new_dist = dist_here + cheat_length + dist_from_end[nr][nc]
                    saving = base_dist - new_dist
                    if saving >= saving_threshold:
                        count += 1

    return count


# ---------------------------------------------------------------------------
# Parte 2 – cheat fino a 20 passi
# ---------------------------------------------------------------------------

def solve_2(test_string: str | None = None) -> int:
    """
    Conta quanti cheat (segmenti di lunghezza <= 20 passi ignorando muri)
    permettono di risparmiare almeno:
      - 70 picosecondi sul sample
      - 100 picosecondi sull'input reale.
    Ogni cheat è identificato da una coppia ((r1,c1),(r2,c2)).
    """
    raw = GI.input if test_string is None else test_string
    grid, start, end = parse_grid(raw)
    H, W = len(grid), len(grid[0])

    dist_from_start = bfs_no_cheat(grid, start)
    dist_from_end = bfs_no_cheat(grid, end)
    base_dist = dist_from_start[end[0]][end[1]]

    if base_dist < 0:
        return 0

    saving_threshold = 70 if test_string is not None else 100
    max_cheat_len = 20

    found_cheats: set[tuple[Pos, Pos]] = set()

    for r in range(H):
        for c in range(W):
            if dist_from_start[r][c] < 0:
                continue
            if grid[r][c] == "#":
                continue

            base_dist_here = dist_from_start[r][c]

            # Considera tutte le celle entro distanza di Manhattan <= 20
            for dr in range(-max_cheat_len, max_cheat_len + 1):
                max_dc = max_cheat_len - abs(dr)
                for dc in range(-max_dc, max_dc + 1):
                    if dr == 0 and dc == 0:
                        continue
                    cheat_len = abs(dr) + abs(dc)
                    if cheat_len == 0 or cheat_len > max_cheat_len:
                        continue

                    nr, nc = r + dr, c + dc
                    if not in_bounds(nr, nc, H, W):
                        continue
                    if grid[nr][nc] == "#":
                        continue
                    if dist_from_end[nr][nc] < 0:
                        continue

                    new_dist = base_dist_here + cheat_len + dist_from_end[nr][nc]
                    saving = base_dist - new_dist
                    if saving >= saving_threshold:
                        found_cheats.add(((r, c), (nr, nc)))

    return len(found_cheats)


if __name__ == "__main__":
    test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

    print("Test Part 1:", solve_1(test))
    print("Test Part 2:", solve_2(test))

    print("Part 1 (input reale):", solve_1())
    print("Part 2 (input reale):", solve_2())
