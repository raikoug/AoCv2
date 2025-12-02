from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

TIME = 2503


def calc_distance(speed: int, sprint: int, rest: int, time: int = TIME) -> int:
    """Distanza percorsa da una renna dopo `time` secondi."""
    seconds = 0
    running = True
    distance = 0

    while seconds < time:
        if running:
            chunk = min(sprint, time - seconds)
            distance += chunk * speed
            seconds += chunk
            running = False
        else:
            chunk = min(rest, time - seconds)
            seconds += chunk
            running = True

    return distance


@dataclass
class Deer:
    name: str
    speed: int
    sprint: int
    rest: int
    points: int = 0

    @classmethod
    def from_line(cls, line: str) -> "Deer":
        # Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        sprint = int(parts[6])
        rest = int(parts[13])
        return cls(name=name, speed=speed, sprint=sprint, rest=rest)

    def distance_after(self, time: int) -> int:
        return calc_distance(self.speed, self.sprint, self.rest, time)


@dataclass
class Race:
    total_time: int = TIME
    deers: Dict[str, Deer] = None

    def __post_init__(self) -> None:
        if self.deers is None:
            self.deers = {}

    def add_deer(self, line: str) -> None:
        deer = Deer.from_line(line)
        self.deers[deer.name] = deer

    def tick(self, second: int) -> None:
        """Aggiorna i punti al secondo `second` (1-based)."""
        distances: Dict[str, int] = {}
        best_distance = 0

        for name, deer in self.deers.items():
            d = deer.distance_after(second)
            distances[name] = d
            if d > best_distance:
                best_distance = d

        # Tutti i leader in questo secondo prendono un punto
        for name, d in distances.items():
            if d == best_distance:
                self.deers[name].points += 1

    def run(self) -> None:
        for s in range(1, self.total_time + 1):
            self.tick(s)


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    best = 0
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        speed = int(parts[3])
        sprint = int(parts[6])
        rest = int(parts[13])
        distance = calc_distance(speed, sprint, rest)
        if distance > best:
            best = distance
    return best


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    race = Race()
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        race.add_deer(line)
    race.run()
    return max(deer.points for deer in race.deers.values())


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
