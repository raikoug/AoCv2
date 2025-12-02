from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


# Direzioni: freccia -> (delta_row, delta_col)
DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "→": (0, 1),
    "←": (0, -1),
    "↑": (-1, 0),
    "↓": (1, 0),
}


@dataclass
class Tile:
    row: int
    col: int
    symbol: str
    energized_from: Set[str] = field(default_factory=set)

    def add_energy(self, direction: str) -> bool:
        """
        Registra che un raggio è passato da questa tile in `direction`.
        Restituisce True se è la prima volta da quella direzione, False altrimenti.
        """
        if direction in self.energized_from:
            return False
        self.energized_from.add(direction)
        return True


@dataclass
class Beam:
    row: int
    col: int
    direction: str  # "→", "←", "↑", "↓"


class Game:
    def __init__(self, lines: List[str]) -> None:
        self.rows = len(lines)
        self.cols = len(lines[0]) if self.rows > 0 else 0
        self.tiles: List[List[Tile]] = [
            [Tile(r, c, ch) for c, ch in enumerate(line)]
            for r, line in enumerate(lines)
        ]
        self.beams: List[Beam] = []

    def _step(self) -> None:
        new_beams: List[Beam] = []

        while self.beams:
            beam = self.beams.pop()
            dr, dc = DIRECTIONS[beam.direction]
            nr, nc = beam.row + dr, beam.col + dc

            # Fuori dalla griglia: il raggio si estingue
            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                continue

            tile = self.tiles[nr][nc]

            # Se abbiamo già energizzato questa tile da questa direzione, interrompi
            if not tile.add_energy(beam.direction):
                continue

            ch = tile.symbol

            if ch == ".":
                new_beams.append(Beam(nr, nc, beam.direction))
            elif ch == "/":
                new_dir = {
                    "→": "↑",
                    "↑": "→",
                    "←": "↓",
                    "↓": "←",
                }[beam.direction]
                new_beams.append(Beam(nr, nc, new_dir))
            elif ch == "\\":
                new_dir = {
                    "→": "↓",
                    "↓": "→",
                    "←": "↑",
                    "↑": "←",
                }[beam.direction]
                new_beams.append(Beam(nr, nc, new_dir))
            elif ch == "|":
                if beam.direction in ("↑", "↓"):
                    new_beams.append(Beam(nr, nc, beam.direction))
                else:
                    # Split in alto e in basso
                    new_beams.append(Beam(nr, nc, "↑"))
                    new_beams.append(Beam(nr, nc, "↓"))
            elif ch == "-":
                if beam.direction in ("←", "→"):
                    new_beams.append(Beam(nr, nc, beam.direction))
                else:
                    # Split a sinistra e destra
                    new_beams.append(Beam(nr, nc, "←"))
                    new_beams.append(Beam(nr, nc, "→"))
            else:
                # Qualsiasi altro carattere è trattato come muro: il raggio si ferma
                continue

        self.beams = new_beams

    def run(self) -> None:
        while self.beams:
            self._step()

    def energized_count(self) -> int:
        return sum(1 for row in self.tiles for tile in row if tile.energized_from)


def _run_game(lines: List[str], start_row: int, start_col: int, direction: str) -> int:
    game = Game(lines)
    game.beams.append(Beam(start_row, start_col, direction))
    game.run()
    return game.energized_count()


def _calculate_beam_starts(lines: List[str]) -> List[Tuple[int, int, str]]:
    """
    Genera tutte le possibili posizioni di partenza dei raggi sui bordi
    della griglia, come richiesto per la parte 2.
    """
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0
    starts: List[Tuple[int, int, str]] = []

    # Da sinistra e destra
    for r in range(rows):
        starts.append((r, -1, "→"))      # da sinistra verso destra
        starts.append((r, cols, "←"))    # da destra verso sinistra

    # Dall'alto e dal basso
    for c in range(cols):
        starts.append((-1, c, "↓"))      # dall'alto verso il basso
        starts.append((rows, c, "↑"))    # dal basso verso l'alto

    return starts


def solve_1(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = raw.splitlines()
    # Partiamo appena fuori dalla griglia, in alto a sinistra, puntando a destra
    return _run_game(lines, start_row=0, start_col=-1, direction="→")


def solve_2(test_string: str | None = None) -> int:
    raw = GI.input if test_string is None else test_string
    lines = raw.splitlines()

    best = 0
    for r, c, direction in _calculate_beam_starts(lines):
        energized = _run_game(lines, start_row=r, start_col=c, direction=direction)
        if energized > best:
            best = energized

    return best


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
