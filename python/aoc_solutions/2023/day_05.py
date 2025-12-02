from __future__ import annotations

from pathlib import Path
import re
import sys
from dataclasses import dataclass
from typing import Optional, List, Tuple

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


@dataclass(frozen=True)
class MapRange:
    dest_start: int
    src_start: int
    length: int

    @property
    def src_end(self) -> int:
        return self.src_start + self.length - 1


@dataclass(frozen=True)
class SeedRange:
    start: int
    end: int  # inclusivo


def _parse_maps(lines: List[str]) -> List[List[MapRange]]:
    """Parsa i blocchi 'xxx-to-yyy map:' in una lista di liste di MapRange."""
    maps: List[List[MapRange]] = []
    current: List[MapRange] | None = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith("map:"):
            current = []
            maps.append(current)
        else:
            parts = line.split()
            if len(parts) != 3:
                continue
            dest, src, length = (int(x) for x in parts)
            assert current is not None
            current.append(MapRange(dest_start=dest, src_start=src, length=length))

    return maps


def _apply_one_map(value: int, ranges: List[MapRange]) -> int:
    for mr in ranges:
        if mr.src_start <= value <= mr.src_end:
            return mr.dest_start + (value - mr.src_start)
    return value


def _apply_all_maps(value: int, maps: List[List[MapRange]]) -> int:
    for ranges in maps:
        value = _apply_one_map(value, ranges)
    return value


def solve_1(test_string: Optional[str] = None) -> int:
    """Part 1: trova la location minima applicando le mappe a ogni seed singolo."""
    raw = GI.input if test_string is None else test_string
    lines = [ln.rstrip("\n") for ln in raw.splitlines() if ln.rstrip("\n")]

    # riga seeds
    seeds_line = lines[0]
    seeds = [int(x) for x in seeds_line.split(":", 1)[1].split() if x]

    # mappe
    maps = _parse_maps(lines[1:])

    locations = [_apply_all_maps(seed, maps) for seed in seeds]
    return min(locations)


# ---- Part 2 helpers ----


@dataclass
class MapRange2:
    difference: int
    source_start: int
    source_end: int


def _parse_seed_ranges_and_maps(raw: str) -> Tuple[List[SeedRange], List[List[MapRange2]]]:
    seeds: List[SeedRange] = []
    seed_maps: List[List[MapRange2]] = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("seeds:"):
            for start_str, length_str in re.findall(r"(\d+)\s+(\d+)", line):
                start = int(start_str)
                length = int(length_str)
                seeds.append(SeedRange(start=start, end=start + length - 1))
        elif line.endswith("map:"):
            seed_maps.append([])
        else:
            m = re.match(r"(\d+)\s+(\d+)\s+(\d+)", line)
            if not m:
                continue
            dest = int(m.group(1))
            src = int(m.group(2))
            span = int(m.group(3))
            # difference = source - dest (per usare la formula original seed_2)
            diff = src - dest
            seed_maps[-1].append(
                MapRange2(
                    difference=diff,
                    source_start=src,
                    source_end=src + span - 1,
                )
            )

    for sm in seed_maps:
        sm.sort(key=lambda r: r.source_start)

    return seeds, seed_maps


def solve_2(test_string: Optional[str] = None) -> int:
    """Part 2: usa i range di seed (start, length) e propaga gli intervalli
    attraverso tutte le mappe, restituendo la location minima.
    """
    raw = GI.input if test_string is None else test_string
    seeds, seed_maps = _parse_seed_ranges_and_maps(raw)

    these_ranges: List[SeedRange] = seeds

    for seed_map in seed_maps:
        next_ranges: List[SeedRange] = []
        # Per ogni range corrente, applichiamo le trasformazioni del blocco
        for seed in these_ranges:
            current_start = seed.start
            while current_start <= seed.end:
                mapped = False
                for single_map in seed_map:
                    possible_start = max(single_map.source_start, current_start)
                    if possible_start > seed.end:
                        break
                    possible_end = min(single_map.source_end, seed.end)
                    if possible_end >= possible_start:
                        # parte non mappata prima di possible_start
                        if current_start < possible_start:
                            next_ranges.append(SeedRange(start=current_start, end=possible_start - 1))
                        # parte mappata
                        start_mapped = possible_start - single_map.difference
                        end_mapped = possible_end - single_map.difference
                        next_ranges.append(SeedRange(start=start_mapped, end=end_mapped))
                        current_start = possible_end + 1
                        mapped = True
                        break
                if not mapped:
                    # nessuna mappa applicabile a current_start: il resto del range passa invariato
                    next_ranges.append(SeedRange(start=current_start, end=seed.end))
                    break
        these_ranges = next_ranges

    # location minima è l'inizio minimo dei range finali
    return min(r.start for r in these_ranges)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
