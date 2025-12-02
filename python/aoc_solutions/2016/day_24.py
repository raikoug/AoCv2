from __future__ import annotations

from pathlib import Path
import sys
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict, Iterable, Iterator
from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import PriorityQueue


# Animation Libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from typing import TypedDict

class PathInfo(TypedDict):
    cost: int
    path: list["Point"]

class RouteFrame(TypedDict):
    cost: int
    route_nodes: list[int]
    route_points: list["Point"]
    complete: bool

BfsFromStart = dict[int, PathInfo]
AllBfsResults = dict[int, tuple[BfsFromStart, list["Point"]]]

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


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

@dataclass(frozen=True)
class Node:
    id: int


@dataclass(order=True, frozen=True)
class Edge:
    cost: int
    a: Node = field(compare=False)
    b: Node = field(compare=False)
    path: tuple["Point", ...] = field(compare=False)

    def endpoints(self) -> tuple[Node, Node]:
        return (self.a, self.b)


class Graph:
    """
    Grafo pesato, opzionalmente diretto, con nodi identificati da int.

    Per il day 24: grafo non diretto, full mesh,
    con costi e path derivati dalle BFS sulla griglia.
    """

    def __init__(self, node_ids: Iterable[int], directed: bool = False) -> None:
        self.directed = directed
        # id -> Node
        self.nodes: Dict[int, Node] = {i: Node(i) for i in node_ids}
        # adjacency: id -> {neighbor_id -> PathInfo}
        self._adj: Dict[int, Dict[int, PathInfo]] = {i: {} for i in node_ids}

    def add_edge(self, u: int, v: int, cost: int, path: list["Point"]) -> None:
        """
        Aggiunge (o aggiorna) un arco u-v con dato costo e path da u a v.

        Se il grafo non è diretto, aggiunge anche v-u con path invertito.
        Ignora self-loop (u == v), che non servono per il TSP.
        """
        if u == v:
            return

        self._adj[u][v] = {"cost": cost, "path": path}

        if not self.directed:
            # path inverso da v a u
            rev_path = list(reversed(path))
            self._adj[v][u] = {"cost": cost, "path": rev_path}

    def neighbors(self, u: int) -> Dict[int, PathInfo]:
        """Restituisce i vicini di u come {neighbor_id: PathInfo}."""
        return self._adj[u]

    def get_cost(self, u: int, v: int) -> int:
        """Costo dell'arco u-v (KeyError se non esiste)."""
        return self._adj[u][v]["cost"]

    def get_path(self, u: int, v: int) -> list["Point"]:
        """
        Path dal nodo u al nodo v come lista di Point.

        Attenzione: la lista restituita è quella memorizzata.
        Se vuoi essere sicuro di non modificarla, fai una copy.
        """
        return self._adj[u][v]["path"]

    def __iter__(self) -> Iterator[Node]:
        """Itera sui nodi del grafo."""
        return iter(self.nodes.values())

    def __len__(self) -> int:
        return len(self.nodes)

    # --- Arci come oggetti Edge -------------------------------------------

    def edges(self) -> list[Edge]:
        """
        Restituisce la lista di Edge.

        Per grafi non diretti, ogni arco compare una sola volta
        (no duplicati u-v e v-u).
        """
        edges: list[Edge] = []
        seen: set[tuple[int, int]] = set()

        for u, nbrs in self._adj.items():
            for v, info in nbrs.items():
                cost = info["cost"]
                path = tuple(info["path"])
                if self.directed:
                    edges.append(Edge(cost, self.nodes[u], self.nodes[v], path))
                else:
                    a, b = sorted((u, v))
                    key = (a, b)
                    if key not in seen:
                        seen.add(key)
                        # vogliamo path da a -> b
                        if u == a and v == b:
                            path_ab = path
                        else:
                            path_ab = tuple(reversed(path))
                        edges.append(Edge(cost, self.nodes[a], self.nodes[b], path_ab))
        return edges

    # --- Costruttore dal mondo "labirinto + BFS" ---------------------------

    @classmethod
    def from_bfs_results(
        cls,
        bfs_results: AllBfsResults,
        directed: bool = False,
    ) -> "Graph":
        """
        Costruisce un grafo pesato a partire dai risultati delle BFS.

        bfs_results:
            start_id -> ( { target_id: PathInfo }, frames )
        """
        node_ids = list(bfs_results.keys())
        g = cls(node_ids, directed=directed)

        for start_id, (targets, _frames) in bfs_results.items():
            for target_id, info in targets.items():
                cost = info["cost"]
                path = info["path"]
                g.add_edge(start_id, target_id, cost, path)

        return g

def find_best_path(grid: Grid, start: Point, total_nodes: int) -> tuple[BfsFromStart, list[Point]]:
    result: BfsFromStart = dict()
    visited: set = set()
    seq = 0
    path : list = list()
    frames: list[Point] = list()

    q = PriorityQueue()

    # queue data format: [cost, tiebreaker, Point, path_to_here]

    # Idea:
    # - get next queue element with priority
    # - check if element is a node, and append to result (should be the best..)
    # - list walkable paths
    # - remove the visited ones
    # - add to the queue all the walkable nodes filtered
    # - repeat
    
    q.put([0,seq, start, path])
    frames.append(start)
    seq += 1

    while not q.empty():
        cost: int
        point: Point
        cost,_,point,path = q.get()
        frames.append(point)

        if (point.is_node) and (point.node != start.node):
            if point.node:
                result[point.node] = {
                    "cost": cost,
                    "path": path
                }
        
        if len(result) == total_nodes:
            return (result, frames)

        possible_paths = grid.get_walkable(point)

        for next_point in [possible_point for possible_point in possible_paths if possible_point not in visited]:
            visited.add(next_point)
            new_path = path.copy()
            new_path.append(next_point)
            q.put([cost+1, seq, next_point, new_path])
            seq += 1

    return (result, frames)

def find_best_tour(
    graph: Graph,
    start_id: int = 0,
    go_back: bool = False,
) -> tuple[list[int], int, list[RouteFrame]]:
    """
    Find the cheapest route on the graph starting from `start_id`.

    If go_back is False:
      - route must visit all nodes exactly once (start included).
    If go_back is True:
      - route must visit all nodes and finally go back to start_id.

    We use a uniform-cost search (Dijkstra-like) over the space of tours:
    - state = (current_node, visited_set, cost_so_far, route_nodes, route_points)
    - priority queue ordered by cost_so_far
    - the first state that satisfies the goal condition is optimal.
    """

    total_nodes: int = len(graph)
    if start_id not in graph.nodes:
        raise ValueError(f"Start node {start_id} not in graph")

    best_route_nodes: list[int] = []
    best_cost: int = 0
    frames: list[RouteFrame] = []

    # queue data format:
    # [cost_so_far, tie_breaker, current_node_id, visited_set, route_nodes, route_points]
    q: PriorityQueue = PriorityQueue()
    seq = 0  # tie-breaker for stable ordering

    # initial state
    start_visited = {start_id}
    start_route_nodes: list[int] = [start_id]
    start_route_points: list[Point] = []  # will be built as we move between nodes

    q.put([0, seq, start_id, start_visited, start_route_nodes, start_route_points])
    seq += 1

    while not q.empty():
        cost: int
        current_id: int
        visited: set[int]
        route_nodes: list[int]
        route_points: list[Point]

        cost, _, current_id, visited, route_nodes, route_points = q.get()

        # goal check depends on go_back flag
        is_complete = (
            len(visited) == total_nodes
            if not go_back
            else (len(visited) == total_nodes and current_id == start_id)
        )

        # record this state as a graph-frame (for future visualization)
        frame: RouteFrame = {
            "cost": cost,
            "route_nodes": list(route_nodes),
            "route_points": list(route_points),
            "complete": is_complete,
        }
        frames.append(frame)

        # if this state satisfies the goal condition, we are done
        if is_complete:
            best_route_nodes = route_nodes
            best_cost = cost
            break

        # expand neighbors
        for neighbor_id, info in graph.neighbors(current_id).items():
            edge_cost: int = info["cost"]
            segment_path: list[Point] = info["path"]  # path from current_id -> neighbor_id

            # special handling for start_id when go_back=True:
            # we want to allow exactly one final step back to start
            if neighbor_id == start_id:
                if not go_back:
                    # when go_back is False, we never revisit the start node
                    continue
                # when go_back is True, we only allow going back to start
                # after all nodes have been visited
                if len(visited) != total_nodes:
                    continue

                new_cost = cost + edge_cost
                new_visited = set(visited)  # same set, all nodes already visited
                new_route_nodes = list(route_nodes)
                new_route_nodes.append(start_id)

                if route_points:
                    new_route_points = list(route_points)
                    new_route_points.extend(segment_path[1:])
                else:
                    new_route_points = list(segment_path)

                q.put([new_cost, seq, start_id, new_visited, new_route_nodes, new_route_points])
                seq += 1
                continue

            # regular neighbors (not the start node)
            if neighbor_id in visited:
                # do not revisit already visited nodes
                continue

            new_cost = cost + edge_cost

            # clone and extend visited set
            new_visited = set(visited)
            new_visited.add(neighbor_id)

            # clone and extend route in terms of node ids
            new_route_nodes = list(route_nodes)
            new_route_nodes.append(neighbor_id)

            # extend the physical path in the maze:
            # first segment: we keep the full path
            # next segments: skip the first point to avoid duplicating joints
            if route_points:
                new_route_points = list(route_points)
                new_route_points.extend(segment_path[1:])
            else:
                new_route_points = list(segment_path)

            q.put([new_cost, seq, neighbor_id, new_visited, new_route_nodes, new_route_points])
            seq += 1

    return best_route_nodes, best_cost, frames

def solve_1(test_string: str | None = None) -> tuple[int,int]:
    inputs_1 = GI.input if test_string is None else test_string

    grid = Grid(inputs_1)
    total_nodes: int = len(grid.nodes) - 1
    BFSresults: AllBfsResults = {}

    with ProcessPoolExecutor() as executor:

        futures = {
            executor.submit(find_best_path, grid, start, total_nodes): start 
            for start in grid.nodes.values()
            }


        for future in as_completed(futures):
            start = futures[future]
            paths = future.result()
            assert start.node is not None
            BFSresults[start.node] = paths

    graph = Graph.from_bfs_results(BFSresults, directed=False)

    best_route_nodes_1, best_cost_1, frames_1 = find_best_tour(graph, 0)
    best_route_nodes_2, best_cost_2, frames_2 = find_best_tour(graph, 0, True)

    #anim = animate_bfs(grid, BFSresults, interval=5, frame_step=10, save_path=None)
    #plt.show()


    return best_cost_1, best_cost_2


# def animate_bfs(
#     grid: "Grid",
#     results: Dict[int, Tuple[BfsFromStart, List["Point"]]],
#     interval: int = 50,
#     frame_step: int = 1,
#     save_path: str | None = None,
# ) -> FuncAnimation:
#     """
#     Animazione cyberpunk delle BFS per ogni nodo di partenza.

#     Parameters
#     ----------
#     grid : Grid
#         La griglia che hai usato per calcolare le BFS.
#     results : dict[int, (dict[int, dict], list[Point])]
#         start_node -> (distanze, frames_di_visita_in_ordine).
#     interval : int, default 50
#         Millisecondi tra un frame e l'altro (~20 fps).
#     frame_step : int, default 1
#         Di quanti passi logici della BFS avanzare tra un frame e il successivo.
#         Es: 5 = mostra uno step ogni 5 visite.
#     save_path : str | None, default None
#         Se None, mostra solo l'animazione a schermo (plt.show()).
#         Se un path (es. "bfs.mp4" o "bfs.gif"), salva il file.

#     Returns
#     -------
#     anim : matplotlib.animation.FuncAnimation
#         L'oggetto animazione (mantienilo in vita finché serve).
#     """

#     if frame_step <= 0:
#         raise ValueError("frame_step must be >= 1")

#     # ---- 1. Dimensioni della griglia ---------------------------------------
#     height = len(grid)
#     if height == 0:
#         raise ValueError("Grid is empty")
#     width = len(grid[0])

#     # ---- 2. Mappa base (0 = muro, 1 = walkable, 2 = nodo) ------------------
#     base = np.zeros((height, width), dtype=np.uint8)
#     for r in range(height):
#         for c in range(width):
#             p: "Point" = grid[r][c]
#             if p.is_wall:
#                 base[r, c] = 0
#             elif p.is_node:
#                 base[r, c] = 2
#             elif p.can_walk:
#                 base[r, c] = 1
#             else:
#                 base[r, c] = 0  # fallback

#     # ---- 3. Pre-elaborazione dei frames: visit_step per ogni start ---------
#     start_ids = sorted(results.keys())
#     num_starts = len(start_ids)
#     if num_starts == 0:
#         raise ValueError("No BFS results to animate")

#     visit_steps: Dict[int, Tuple[np.ndarray, int]] = {}
#     max_len = 0

#     for start_id in start_ids:
#         bfs_data, frames = results[start_id]   # bfs_data: dict[int, PathInfo], qui non ti serve ancora
#         vs = np.full((height, width), -1, dtype=np.int32)
#         for step, p in enumerate(frames):
#             vs[p.row, p.col] = step
#         visit_steps[start_id] = (vs, len(frames))
#         max_len = max(max_len, len(frames))


#     # numero di frame grafici in base allo step
#     total_frames = math.ceil(max_len / frame_step) + 5

#     # ---- 4. Layout subplot (3 colonne, righe dinamiche) --------------------
#     cols = min(3, num_starts)
#     rows = math.ceil(num_starts / cols)

#     width_per_panel = 6.0
#     height_per_panel = 3.5
#     figsize = (cols * width_per_panel, rows * height_per_panel)

#     fig, axes = plt.subplots(
#         rows,
#         cols,
#         figsize=figsize,
#         constrained_layout=True,
#     )
#     fig.patch.set_facecolor("#050010")

#     try:
#         manager = plt.get_current_fig_manager()
#         if hasattr(manager, "full_screen_toggle"):
#             manager.full_screen_toggle()
#         else:
#             try:
#                 manager.window.showMaximized()
#             except Exception:
#                 pass
#     except Exception:
#         pass

#     if isinstance(axes, np.ndarray):
#         axes_list = axes.flatten().tolist()
#     else:
#         axes_list = [axes]

#     # ---- 5. Palette cyberpunk ----------------------------------------------
#     wall_color    = np.array([5, 0, 16])    / 255.0  # #050010
#     floor_color   = np.array([10, 5, 40])   / 255.0  # blu-viola scuro
#     node_color    = np.array([255, 230, 0]) / 255.0  # giallo neon
#     visited_color = np.array([0, 245, 255]) / 255.0  # teal
#     head_color    = np.array([255, 50, 255]) / 255.0 # magenta

#     # ---- 6. Immagine per ogni start ----------------------------------------
#     images: Dict[int, plt.AxesImage] = {}

#     for ax, start_id in zip(axes_list, start_ids):
#         ax.set_facecolor("#020010")
#         ax.set_xticks([])
#         ax.set_yticks([])
#         ax.set_title(
#             f"Start {start_id}",
#             color=visited_color,
#             fontsize=14,
#             pad=10,
#         )

#         img_data = np.zeros((height, width, 3), dtype=float)
#         img = ax.imshow(img_data, interpolation="nearest", animated=True)
#         images[start_id] = img

#     for ax in axes_list[len(start_ids):]:
#         ax.axis("off")

#     # ---- 7. Costruzione del frame per uno start ---------------------------
#     def make_rgb_for_start(start_id: int, frame_idx: int) -> np.ndarray:
#         vs, length = visit_steps[start_id]

#         if length == 0:
#             t = -1
#         else:
#             logical_t = frame_idx * frame_step
#             t = min(logical_t, length - 1)

#         rgb = np.zeros((height, width, 3), dtype=float)

#         rgb[base == 0] = wall_color
#         rgb[base == 1] = floor_color
#         rgb[base == 2] = node_color

#         if t < 0:
#             return rgb

#         visited_mask = (vs >= 0) & (vs <= t)
#         head_mask = (vs == t)

#         rgb[visited_mask] = visited_color
#         rgb[head_mask] = head_color

#         return rgb

#     # ---- 8. Update per FuncAnimation --------------------------------------
#     def update(frame_idx: int):
#         artists = []
#         for start_id, img in images.items():
#             rgb = make_rgb_for_start(start_id, frame_idx)
#             img.set_data(rgb)
#             artists.append(img)
#         return artists

#     anim = FuncAnimation(
#         fig,
#         update,
#         frames=total_frames,
#         interval=interval,
#         blit=True,
#         repeat=True,
#     )

#     if save_path is not None:
#         fps = max(1, int(1000 / interval)) if interval > 0 else 20
#         anim.save(save_path, fps=fps)

#     return anim

if __name__ == "__main__":
    part1,part2 = solve_1()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
