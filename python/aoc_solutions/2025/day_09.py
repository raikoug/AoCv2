from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput
from typing import TypeAlias, Sequence, Callable
from collections import deque
from multiprocessing import Pool, cpu_count


GI = GetInput()

corner : TypeAlias = tuple[int,int]
Corner : TypeAlias = tuple[int, int]

Area : Callable[[corner,corner], int] = lambda a,b : (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)



def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    corners : list[tuple[int,int]] = list()
    max_area: int = 0
    for line in inputs_1.strip().splitlines():
        x,y = line.split(",")
        corner = (int(x), int(y))
        for c in corners:
            area: int = Area(corner, c)
            if area > max_area:
                max_area = area
        corners.append(corner)

    
    return max_area

def point_in_polygon(point: Corner, vertices: Sequence[Corner]) -> bool:
    """
    Restituisce True se il punto è dentro o sul bordo del poligono
    definito dai vertici (in ordine), usando ray casting orizzontale verso sinistra.
    """
    cx, cy = point
    n = len(vertices)
    crossings = 0

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        # Punto esattamente su un bordo verticale
        if x1 == x2 == cx:
            if min(y1, y2) <= cy <= max(y1, y2):
                return True

        # Punto esattamente su un bordo orizzontale
        if y1 == y2 == cy:
            if min(x1, x2) <= cx <= max(x1, x2):
                return True

        # Ray casting: contiamo le intersezioni del raggio orizzontale a sinistra
        # con i lati verticali del poligono
        if x1 == x2:  # lato verticale
            edge_x = x1
            edge_min_y = min(y1, y2)
            edge_max_y = max(y1, y2)

            # lato a sinistra del punto e che "taglia" il raggio
            if edge_x < cx and edge_min_y < cy <= edge_max_y:
                crossings += 1

    # dispari → dentro; pari → fuori
    return crossings % 2 == 1


def edge_crosses_rectangle(p1: Corner, p2: Corner,
                           min_x: int, max_x: int,
                           min_y: int, max_y: int) -> bool:
    """
    Restituisce True se il segmento p1-p2 (asse allineato)
    attraversa l'interno del rettangolo (min_x..max_x, min_y..max_y).
    Sono ammessi contatti sul bordo, ma non attraversamenti interni.
    """
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        # lato verticale
        edge_x = x1
        edge_min_y = min(y1, y2)
        edge_max_y = max(y1, y2)

        # il lato ha x interno al rettangolo
        if min_x < edge_x < max_x:
            # e la proiezione in y sovrappone quella del rettangolo
            if edge_min_y < max_y and edge_max_y > min_y:
                return True

    elif y1 == y2:
        # lato orizzontale
        edge_y = y1
        edge_min_x = min(x1, x2)
        edge_max_x = max(x1, x2)

        # il lato ha y interna al rettangolo
        if min_y < edge_y < max_y:
            # e la proiezione in x sovrappone quella del rettangolo
            if edge_min_x < max_x and edge_max_x > min_x:
                return True

    return False


def rectangle_inside_region(min_x: int, max_x: int,
                            min_y: int, max_y: int,
                            vertices: Sequence[Corner],
                            edges: Sequence[tuple[Corner, Corner]]) -> bool:
    """
    True se il rettangolo axis-aligned [min_x..max_x] × [min_y..max_y]
    è completamente dentro (o sul bordo) del poligono definito da vertices.
    """
    # 1) tutti e 4 gli angoli dentro o sul bordo
    corners = [
        (min_x, min_y),
        (min_x, max_y),
        (max_x, min_y),
        (max_x, max_y),
    ]
    for cx, cy in corners:
        if not point_in_polygon((cx, cy), vertices):
            return False

    # 2) nessun lato del poligono attraversa l'interno del rettangolo
    for p1, p2 in edges:
        if edge_crosses_rectangle(p1, p2, min_x, max_x, min_y, max_y):
            return False

    return True

def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    # parse input in lista di corner (x, y)
    vertices: list[Corner] = []
    for line in inputs_1.strip().splitlines():
        x_str, y_str = line.split(",")
        vertices.append((int(x_str), int(y_str)))

    n: int = len(vertices)

    # costruisci i lati del poligono (loop chiuso)
    edges: list[tuple[Corner, Corner]] = []
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        edges.append((p1, p2))

    max_area: int = 0

    # tutte le coppie di red tiles come angoli opposti
    for i in range(n):
        x1, y1 = vertices[i]
        for j in range(i + 1, n):
            x2, y2 = vertices[j]

            # se condividono x o y → rettangolo degenerato (area "linea")
            if x1 == x2 or y1 == y2:
                continue

            min_x, max_x = (x1, x2) if x1 <= x2 else (x2, x1)
            min_y, max_y = (y1, y2) if y1 <= y2 else (y2, y1)

            area = (max_x - min_x + 1) * (max_y - min_y + 1)

            # pruning: se non può battere il massimo, salta subito
            if area <= max_area:
                continue

            if rectangle_inside_region(min_x, max_x, min_y, max_y, vertices, edges):
                max_area = area

    return max_area

if __name__ == "__main__":
    test = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
