from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Callable, Final, TypeAlias


PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()

# -----------------------------
# Type aliases (strict-friendly)
# -----------------------------
Coord: TypeAlias = tuple[int, int]
Grid: TypeAlias = tuple[str, ...]
Cells: TypeAlias = frozenset[Coord]
CountsByShape: TypeAlias = dict[int, int]

AreaFn: TypeAlias = Callable[[int, int], int]
area: AreaFn = lambda w, h: w * h


# -----------------------------
# Domain models
# -----------------------------
@dataclass(frozen=True, slots=True)
class Shape:
    shape_id: int
    grid: Grid
    cells: Cells
    width: int
    height: int
    filled_area: int  # number of '#'

    @staticmethod
    def from_grid(shape_id: int, rows: list[str]) -> Shape:
        if not rows:
            raise ValueError(f"Shape {shape_id} has an empty grid.")

        row_len = len(rows[0])
        if row_len == 0:
            raise ValueError(f"Shape {shape_id} has an empty row.")

        for r in rows:
            if len(r) != row_len:
                raise ValueError(
                    f"Shape {shape_id} has inconsistent row lengths: "
                    f"expected {row_len}, got {len(r)}."
                )
            for ch in r:
                if ch not in (".", "#"):
                    raise ValueError(
                        f"Shape {shape_id} contains invalid char {ch!r}. "
                        "Allowed: '.' and '#'."
                    )

        height = len(rows)
        width = row_len

        cells: set[Coord] = set()
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch == "#":
                    cells.add((x, y))

        if not cells:
            raise ValueError(f"Shape {shape_id} has no filled cells ('#').")

        grid_t: Grid = tuple(rows)
        cells_f: Cells = frozenset(cells)

        return Shape(
            shape_id=shape_id,
            grid=grid_t,
            cells=cells_f,
            width=width,
            height=height,
            filled_area=len(cells_f),
        )


@dataclass(frozen=True, slots=True)
class RegionSpec:
    width: int
    height: int
    required: CountsByShape  # only qty > 0, keyed by shape_id
    raw_line: str

    @property
    def region_area(self) -> int:
        return area(self.width, self.height)


@dataclass(frozen=True, slots=True)
class ParsedInput:
    shapes: dict[int, Shape]          # by shape_id
    shape_order: tuple[int, ...]      # stable order used by regions
    regions: list[RegionSpec]


# -----------------------------
# Parsing
# -----------------------------
@dataclass(frozen=True, slots=True)
class InputParser:
    # e.g. "0:" or "12:"
    SHAPE_HEADER_RE: Final[re.Pattern[str]] = re.compile(r"^\s*(\d+)\s*:\s*$")
    # e.g. "12x5: 1 0 1 0 2 2"
    REGION_RE: Final[re.Pattern[str]] = re.compile(r"^\s*(\d+)\s*x\s*(\d+)\s*:\s*(.*)\s*$")

    IntFn: TypeAlias = Callable[[str], int]
    to_int: IntFn = lambda s: int(s)

    def parse(self, raw: str) -> ParsedInput:
        lines = self._split_keep_blanks(raw)

        region_start = self._find_first_region_line(lines)
        shape_lines = lines[:region_start]
        region_lines = lines[region_start:]

        shapes = self._parse_shapes(shape_lines)
        if not shapes:
            raise ValueError("No shapes found in input.")

        shape_order = tuple(sorted(shapes.keys()))

        regions = self._parse_regions(region_lines, shape_order)

        return ParsedInput(shapes=shapes, shape_order=shape_order, regions=regions)

    def _split_keep_blanks(self, raw: str) -> list[str]:
        # keep blank lines because they delimit shapes
        return raw.strip("\n").splitlines()

    def _find_first_region_line(self, lines: list[str]) -> int:
        for i, ln in enumerate(lines):
            if self._is_region_line(ln):
                return i
        raise ValueError("Could not find any region lines (e.g. '12x5: ...') in input.")

    def _is_region_line(self, ln: str) -> bool:
        return self.REGION_RE.match(ln) is not None

    def _parse_shapes(self, lines: list[str]) -> dict[int, Shape]:
        shapes: dict[int, Shape] = {}
        i = 0
        n = len(lines)

        while i < n:
            ln = lines[i].strip()
            if ln == "":
                i += 1
                continue

            m = self.SHAPE_HEADER_RE.match(ln)
            if m is None:
                raise ValueError(f"Expected shape header like 'N:' but got: {lines[i]!r}")

            shape_id = self.to_int(m.group(1))
            if shape_id in shapes:
                raise ValueError(f"Duplicate shape id: {shape_id}")

            i += 1
            rows: list[str] = []
            while i < n and lines[i].strip() != "":
                rows.append(lines[i].strip())
                i += 1

            shapes[shape_id] = Shape.from_grid(shape_id, rows)

            # skip blank separator(s)
            while i < n and lines[i].strip() == "":
                i += 1

        return shapes

    def _parse_regions(self, lines: list[str], shape_order: tuple[int, ...]) -> list[RegionSpec]:
        regions: list[RegionSpec] = []
        expected_counts = len(shape_order)

        for raw_ln in lines:
            ln = raw_ln.strip()
            if ln == "":
                continue

            m = self.REGION_RE.match(ln)
            if m is None:
                raise ValueError(f"Invalid region line: {raw_ln!r}")

            w = self.to_int(m.group(1))
            h = self.to_int(m.group(2))
            rest = m.group(3).strip()

            if w <= 0 or h <= 0:
                raise ValueError(f"Region must be positive-sized, got {w}x{h} in {raw_ln!r}")

            qty_parts = rest.split() if rest else []
            if len(qty_parts) != expected_counts:
                raise ValueError(
                    f"Region {w}x{h} expected {expected_counts} quantities "
                    f"(one per shape id in {shape_order}), got {len(qty_parts)}: {raw_ln!r}"
                )

            required: CountsByShape = {}
            for shape_id, qty_s in zip(shape_order, qty_parts, strict=True):
                qty = self.to_int(qty_s)
                if qty < 0:
                    raise ValueError(f"Negative quantity is not allowed: {raw_ln!r}")
                if qty > 0:
                    required[shape_id] = qty

            regions.append(RegionSpec(width=w, height=h, required=required, raw_line=raw_ln))

        return regions


# -----------------------------
# Solutions (placeholder for now)
# -----------------------------
def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    parser = InputParser()
    parsed = parser.parse(inputs_1)

    # TODO: plug the actual packing solver.
    # For now we just ensure parsing works without exploding.
    _ = (parsed.shapes, parsed.shape_order, parsed.regions)

    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    parser = InputParser()
    parsed = parser.parse(inputs_1)

    # TODO: Part 2 unknown yet (depends on full puzzle).
    _ = (parsed.shapes, parsed.shape_order, parsed.regions)

    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
