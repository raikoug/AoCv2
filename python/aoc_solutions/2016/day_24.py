from __future__ import annotations

from pathlib import Path
import sys
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import PriorityQueue


# Animation Libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


@dataclass
class Direction:
    row: int
    col : int

D: list[Direction] = [
    Direction(1,0),
    Direction(0,1),
    Direction(-1,0),
    Direction(0,-1),
]
class Point():
    row: int
    col: int
    symbol: str
    is_wall: bool
    can_walk: bool
    is_node: bool
    node: Optional[int]

    def __init__(self, char: str, row: int, col: int, 
                 wall: str = "#", space: str = "."):
        self.row = row
        self.col = col
        self.symbol = char
        self.is_wall = True
        self.can_walk = False
        self.is_node = False

        if char.isdigit():
            self.is_node = True
            self.node = int(char)
            self.is_wall = False
            self.can_walk = True
        elif char == space:
            self.is_wall = False
            self.can_walk = True
    
    def __add__(self, other: Direction) -> Tuple[int,int]:
        return (self.row + other.row, self.col + other.col)
    
    def __repr__(self) -> str:
        return self.symbol
    def __format__(self, format_spec: str) -> str:
        return self.symbol
    def __str__(self) -> str:
        return self.symbol
    def __hash__(self) -> int:
        return hash((self.row, self.col))

class Grid(list[list[Point]]):
    nodes: dict
    costs : dict

    def __init__(self, grid_text: str):
        super().__init__()
        self.nodes = dict()
        lines = grid_text.splitlines()
        for line in lines:
            self.append(list())
        for row in range(len(lines)):
            for col in range(len(lines[0])):
                char = lines[row][col]
                point = Point(char,row,col)
                self[row].append(point)
                if point.is_node: self.nodes[point.node] = point
    
    def get_walkable(self, point: Point) -> List[Point]:
        """
        Get walkable points from Point, no diagonal
        """
        
        return [self[row][col] for direction in D for row,col in [point + direction] if self[row][col].can_walk]



def find_best_path(grid: Grid, start: Point, total_nodes: int) -> tuple[dict[int, int], list[Point]]:
    result = dict()
    visited: set = set()
    seq = 0
    frames: list[Point] = list()

    q = PriorityQueue()

    # queue data format: [cost, tiebreaker, Point]

    # Idea:
    # - get next queue element with priority
    # - check if element is a node, and append to result (should be the best..)
    # - list walkable paths
    # - remove the visited ones
    # - add to the queue all the walkable nodes filtered
    # - repeat
    
    q.put([0,seq, start])
    frames.append(start)
    seq += 1

    while not q.empty():
        cost: int
        point: Point
        cost,_,point = q.get()
        frames.append(point)

        if (point.is_node) and (point.node != start.node):
            result[point.node] = cost
        
        if len(result) == total_nodes:
            return (result, frames)

        possible_paths = grid.get_walkable(point)

        for next_point in [possible_point for possible_point in possible_paths if possible_point not in visited]:
            visited.add(next_point)
            q.put([cost+1, seq, next_point])
            seq += 1

    return (result, frames)

def solve_1(test_string: str | None = None) -> int:#
    inputs_1 = GI.input if test_string is None else test_string

    grid = Grid(inputs_1)
    total_nodes: int = len(grid.nodes) - 1
    results: dict[int, tuple[dict[int, int], list[Point]] ] = {}

    with ProcessPoolExecutor() as executor:

        futures = {
            executor.submit(find_best_path, grid, start, total_nodes): start 
            for start in grid.nodes.values()
            }


        for future in as_completed(futures):
            start = futures[future]
            paths = future.result()
            assert start.node is not None
            results[start.node] = paths

    anim = animate_bfs(grid, results, interval=5, save_path=None)
    plt.show()


    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    # TODO: implementare la logica della parte 2
    return 0


def animate_bfs(
    grid: "Grid",
    results: Dict[int, Tuple[Dict[int, int], List["Point"]]],
    interval: int = 50,
    save_path: str | None = None,
) -> FuncAnimation:
    """
    Animazione cyberpunk delle BFS per ogni nodo di partenza.

    Parameters
    ----------
    grid : Grid
        La griglia che hai usato per calcolare le BFS.
    results : dict[int, (dict[int, int], list[Point])]
        start_node -> (distanze, frames_di_visita_in_ordine).
    interval : int, default 50
        Millisecondi tra un frame e l'altro (~20 fps).
    save_path : str | None, default None
        Se None, mostra solo l'animazione a schermo (plt.show()).
        Se un path (es. "bfs.mp4" o "bfs.gif"), salva il file.

    Returns
    -------
    anim : matplotlib.animation.FuncAnimation
        L'oggetto animazione (mantienilo in vita finché serve).
    """

    # ---- 1. Dimensioni della griglia ---------------------------------------
    height = len(grid)
    if height == 0:
        raise ValueError("Grid is empty")
    width = len(grid[0])

    # ---- 2. Mappa base (0 = muro, 1 = walkable, 2 = nodo) ------------------
    base = np.zeros((height, width), dtype=np.uint8)
    for r in range(height):
        for c in range(width):
            p: "Point" = grid[r][c]
            if p.is_wall:
                base[r, c] = 0
            elif p.is_node:
                base[r, c] = 2
            elif p.can_walk:
                base[r, c] = 1
            else:
                base[r, c] = 0  # fallback

    # ---- 3. Pre-elaborazione dei frames: visit_step per ogni start ---------
    start_ids = sorted(results.keys())
    num_starts = len(start_ids)
    if num_starts == 0:
        raise ValueError("No BFS results to animate")

    visit_steps: Dict[int, Tuple[np.ndarray, int]] = {}
    max_len = 0

    for start_id in start_ids:
        _, frames = results[start_id]
        vs = np.full((height, width), -1, dtype=np.int32)
        for step, p in enumerate(frames):
            vs[p.row, p.col] = step
        visit_steps[start_id] = (vs, len(frames))
        max_len = max(max_len, len(frames))

    # qualche frame extra a BFS finite
    total_frames = max_len + 5

    # ---- 4. Layout subplot (3 colonne, righe dinamiche) --------------------
    cols = min(3, num_starts)
    rows = math.ceil(num_starts / cols)

    # pannelli belli grossi: più larghi che alti
    width_per_panel = 6.0   # in inches
    height_per_panel = 3.5  # in inches
    figsize = (cols * width_per_panel, rows * height_per_panel)

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        constrained_layout=True,
    )
    fig.patch.set_facecolor("#050010")  # sfondo globale quasi nero

    # Prova a usare tutto lo schermo (dipende dal backend)
    try:
        manager = plt.get_current_fig_manager()
        # alcuni backend hanno full_screen_toggle
        if hasattr(manager, "full_screen_toggle"):
            manager.full_screen_toggle()
        else:
            # QtAgg, WxAgg, ecc.
            try:
                manager.window.showMaximized()
            except Exception:
                pass
    except Exception:
        # se fallisce, pazienza: resta solo figsize "grosso"
        pass

    # normalizza axes a lista piatta
    if isinstance(axes, np.ndarray):
        axes_list = axes.flatten().tolist()
    else:
        axes_list = [axes]

    # ---- 5. Palette cyberpunk (RGB in [0,1]) -------------------------------
    wall_color    = np.array([5, 0, 16])    / 255.0  # #050010
    floor_color   = np.array([10, 5, 40])   / 255.0  # blu-viola scuro
    node_color    = np.array([255, 230, 0]) / 255.0  # giallo neon
    visited_color = np.array([0, 245, 255]) / 255.0  # teal acceso
    head_color    = np.array([255, 50, 255]) / 255.0 # magenta

    # ---- 6. Immagine per ogni start ---------------------------------------
    images: Dict[int, plt.AxesImage] = {}

    for ax, start_id in zip(axes_list, start_ids):
        ax.set_facecolor("#020010")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(
            f"Start {start_id}",
            color=visited_color,
            fontsize=14,
            pad=10,
        )

        img_data = np.zeros((height, width, 3), dtype=float)
        img = ax.imshow(img_data, interpolation="nearest", animated=True)
        images[start_id] = img

    # nascondi eventuali subplot in più
    for ax in axes_list[len(start_ids):]:
        ax.axis("off")

    # ---- 7. Costruzione del frame per uno start ---------------------------
    def make_rgb_for_start(start_id: int, frame_idx: int) -> np.ndarray:
        vs, length = visit_steps[start_id]

        if length == 0:
            t = -1
        else:
            t = min(frame_idx, length - 1)

        rgb = np.zeros((height, width, 3), dtype=float)

        # base
        rgb[base == 0] = wall_color
        rgb[base == 1] = floor_color
        rgb[base == 2] = node_color

        if t < 0:
            return rgb

        visited_mask = (vs >= 0) & (vs <= t)
        head_mask = (vs == t)

        rgb[visited_mask] = visited_color
        rgb[head_mask] = head_color

        return rgb

    # ---- 8. Funzione di update per FuncAnimation ---------------------------
    def update(frame_idx: int):
        artists = []
        for start_id, img in images.items():
            rgb = make_rgb_for_start(start_id, frame_idx)
            img.set_data(rgb)
            artists.append(img)
        return artists

    anim = FuncAnimation(
        fig,
        update,
        frames=total_frames,
        interval=interval,
        blit=True,
        repeat=True,
    )

    if save_path is not None:
        fps = max(1, int(1000 / interval)) if interval > 0 else 20
        anim.save(save_path, fps=fps)

    return anim


if __name__ == "__main__":
    test: str = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
