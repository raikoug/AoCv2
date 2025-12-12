from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Callable, ClassVar, Final, TypeAlias


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

Mask: TypeAlias = int
Offset: TypeAlias = tuple[int, int]
RegionKey: TypeAlias = tuple[int, int]

AreaFn: TypeAlias = Callable[[int, int], int]
area: AreaFn = lambda w, h: w * h

ToIntFn: TypeAlias = Callable[[str], int]
to_int: ToIntFn = lambda s: int(s)

SetBitFn: TypeAlias = Callable[[Mask, int], Mask]
set_bit: SetBitFn = lambda mask, idx: mask | (1 << idx)


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
# Symmetries (point 2)
# -----------------------------
@dataclass(frozen=True, slots=True)
class Footprint:
    cells: Cells
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class ShapeVariant:
    shape_id: int
    variant_index: int
    cells: Cells
    width: int
    height: int

    @property
    def filled_area(self) -> int:
        return len(self.cells)


@dataclass(frozen=True, slots=True)
class SymmetryGenerator:
    """
    Generates unique orientations (rotations + flips) for a shape.

    We generate the 8 dihedral transforms by:
      - 4 rotations of the original
      - 4 rotations of the horizontally-flipped original
    Then we normalize + dedup by cell set.
    """

    def unique_variants(self, shape: Shape) -> tuple[ShapeVariant, ...]:
        base = Footprint(cells=shape.cells, width=shape.width, height=shape.height)

        fp0 = self._normalize(base)
        fp1 = self._normalize(self._flip_x(fp0))

        seen: set[Cells] = set()
        variants: list[ShapeVariant] = []
        idx = 0

        for start in (fp0, fp1):
            cur = start
            for _ in range(4):
                norm = self._normalize(cur)
                if norm.cells not in seen:
                    seen.add(norm.cells)
                    variants.append(
                        ShapeVariant(
                            shape_id=shape.shape_id,
                            variant_index=idx,
                            cells=norm.cells,
                            width=norm.width,
                            height=norm.height,
                        )
                    )
                    idx += 1
                cur = self._rotate90_cw(cur)

        return tuple(variants)

    def _rotate90_cw(self, fp: Footprint) -> Footprint:
        w = fp.width
        new_cells = frozenset((y, (w - 1) - x) for (x, y) in fp.cells)
        return Footprint(cells=new_cells, width=fp.height, height=fp.width)

    def _flip_x(self, fp: Footprint) -> Footprint:
        w = fp.width
        new_cells = frozenset(((w - 1) - x, y) for (x, y) in fp.cells)
        return Footprint(cells=new_cells, width=fp.width, height=fp.height)

    def _normalize(self, fp: Footprint) -> Footprint:
        if not fp.cells:
            raise ValueError("Cannot normalize an empty footprint.")

        min_x = min(x for (x, _) in fp.cells)
        min_y = min(y for (_, y) in fp.cells)

        shifted = frozenset((x - min_x, y - min_y) for (x, y) in fp.cells)

        max_x = max(x for (x, _) in shifted)
        max_y = max(y for (_, y) in shifted)

        return Footprint(cells=shifted, width=max_x + 1, height=max_y + 1)


# -----------------------------
# Placements (point 3)
# -----------------------------
@dataclass(frozen=True, slots=True)
class GridIndexer:
    width: int
    height: int

    def index_of(self, coord: Coord) -> int:
        x, y = coord
        return y * self.width + x

    def bit_of(self, coord: Coord) -> Mask:
        return 1 << self.index_of(coord)


@dataclass(frozen=True, slots=True)
class Placement:
    placement_id: int  # stable per shape, used to avoid permutations of identical pieces
    shape_id: int
    variant_index: int
    offset: Offset  # (dx, dy)
    mask: Mask
    filled_area: int  # quick access


@dataclass(frozen=True, slots=True)
class PlacementGenerator:
    """
    For a given Region (W x H), generates all valid placements for each shape,
    considering all unique variants (rotations/flips).

    Each placement is represented as a bitmask (Python int).
    Bit index: idx = y*W + x
    """

    def placements_by_shape(
        self,
        region: RegionSpec,
        variants_by_shape: dict[int, tuple[ShapeVariant, ...]],
    ) -> dict[int, tuple[Placement, ...]]:
        indexer = GridIndexer(width=region.width, height=region.height)

        out: dict[int, tuple[Placement, ...]] = {}
        for shape_id, variants in variants_by_shape.items():
            all_placements: list[Placement] = []
            placement_id = 0
            for variant in variants:
                for p in self._placements_for_variant(indexer, variant, placement_id_start=placement_id):
                    all_placements.append(p)
                placement_id = len(all_placements)
            out[shape_id] = tuple(all_placements)

        return out

    def _placements_for_variant(
        self,
        indexer: GridIndexer,
        variant: ShapeVariant,
        placement_id_start: int,
    ) -> list[Placement]:
        W = indexer.width
        H = indexer.height

        if variant.width > W or variant.height > H:
            return []

        placements: list[Placement] = []
        max_dx = W - variant.width
        max_dy = H - variant.height

        pid = placement_id_start
        for dy in range(max_dy + 1):
            for dx in range(max_dx + 1):
                mask: Mask = 0
                for (x, y) in variant.cells:
                    idx = (y + dy) * W + (x + dx)
                    mask = set_bit(mask, idx)

                placements.append(
                    Placement(
                        placement_id=pid,
                        shape_id=variant.shape_id,
                        variant_index=variant.variant_index,
                        offset=(dx, dy),
                        mask=mask,
                        filled_area=variant.filled_area,
                    )
                )
                pid += 1

        return placements


# -----------------------------
# Solver (point 4)
# -----------------------------
@dataclass(frozen=True, slots=True)
class PackingSolver:
    """
    Decides if a region can fit all required presents.

    Core idea:
      - each placement is a bitmask of occupied cells
      - overlap test is (used & placement.mask) != 0
      - MRV heuristic: pick next shape with the fewest feasible placements
      - pruning: remaining_area <= free_cells
      - avoid permutations for identical shapes using placement_id monotonic constraint
    """

    def can_fit(
        self,
        region: RegionSpec,
        required: CountsByShape,
        shapes: dict[int, Shape],
        placements_by_shape: dict[int, tuple[Placement, ...]],
    ) -> bool:
        region_area = region.region_area

        shape_area: dict[int, int] = {sid: s.filled_area for sid, s in shapes.items()}

        remaining_counts: dict[int, int] = dict(required)
        remaining_area = self._required_area(remaining_counts, shape_area)

        # quick impossible checks
        if remaining_area > region_area:
            return False

        for sid, qty in remaining_counts.items():
            if qty <= 0:
                continue
            if sid not in placements_by_shape:
                return False
            if len(placements_by_shape[sid]) == 0:
                return False

        min_pid_by_shape: dict[int, int] = {}
        used: Mask = 0

        return self._dfs(
            used=used,
            remaining_counts=remaining_counts,
            remaining_area=remaining_area,
            region_area=region_area,
            placements_by_shape=placements_by_shape,
            shape_area=shape_area,
            min_pid_by_shape=min_pid_by_shape,
        )

    def _required_area(self, counts: dict[int, int], shape_area: dict[int, int]) -> int:
        total = 0
        for sid, qty in counts.items():
            if qty > 0:
                total += qty * shape_area[sid]
        return total

    def _dfs(
        self,
        used: Mask,
        remaining_counts: dict[int, int],
        remaining_area: int,
        region_area: int,
        placements_by_shape: dict[int, tuple[Placement, ...]],
        shape_area: dict[int, int],
        min_pid_by_shape: dict[int, int],
    ) -> bool:
        if remaining_area == 0:
            return True

        free_cells = region_area - used.bit_count()
        if remaining_area > free_cells:
            return False

        # MRV: choose the next shape with the fewest feasible placements
        chosen_sid: int | None = None
        chosen_candidates: list[Placement] = []
        best_n: int | None = None

        for sid, qty in remaining_counts.items():
            if qty <= 0:
                continue

            min_pid = min_pid_by_shape.get(sid, 0)
            candidates: list[Placement] = []
            for p in placements_by_shape[sid]:
                if p.placement_id < min_pid:
                    continue
                if (used & p.mask) == 0:
                    candidates.append(p)

            n = len(candidates)
            if n == 0:
                return False

            if best_n is None or n < best_n:
                best_n = n
                chosen_sid = sid
                chosen_candidates = candidates

                # can't do better than 1
                if best_n == 1:
                    break

        if chosen_sid is None:
            return False

        sid = chosen_sid
        old_qty = remaining_counts[sid]

        old_min_pid_present = sid in min_pid_by_shape
        old_min_pid = min_pid_by_shape.get(sid, 0)

        # try each feasible placement
        for p in chosen_candidates:
            remaining_counts[sid] = old_qty - 1
            min_pid_by_shape[sid] = p.placement_id + 1

            if self._dfs(
                used=used | p.mask,
                remaining_counts=remaining_counts,
                remaining_area=remaining_area - shape_area[sid],
                region_area=region_area,
                placements_by_shape=placements_by_shape,
                shape_area=shape_area,
                min_pid_by_shape=min_pid_by_shape,
            ):
                return True

            # restore for next candidate
            remaining_counts[sid] = old_qty
            if old_min_pid_present:
                min_pid_by_shape[sid] = old_min_pid
            else:
                del min_pid_by_shape[sid]

        return False


# -----------------------------
# Parsing
# -----------------------------
@dataclass(frozen=True, slots=True)
class InputParser:
    SHAPE_HEADER_RE: ClassVar[re.Pattern[str]] = re.compile(r"^\s*(\d+)\s*:\s*$")
    REGION_RE: ClassVar[re.Pattern[str]] = re.compile(r"^\s*(\d+)\s*x\s*(\d+)\s*:\s*(.*)\s*$")

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

            shape_id = to_int(m.group(1))
            if shape_id in shapes:
                raise ValueError(f"Duplicate shape id: {shape_id}")

            i += 1
            rows: list[str] = []
            while i < n and lines[i].strip() != "":
                rows.append(lines[i].strip())
                i += 1

            shapes[shape_id] = Shape.from_grid(shape_id, rows)

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

            w = to_int(m.group(1))
            h = to_int(m.group(2))
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
                qty = to_int(qty_s)
                if qty < 0:
                    raise ValueError(f"Negative quantity is not allowed: {raw_ln!r}")
                if qty > 0:
                    required[shape_id] = qty

            regions.append(RegionSpec(width=w, height=h, required=required, raw_line=raw_ln))

        return regions


# -----------------------------
# Solutions
# -----------------------------
def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    parsed = InputParser().parse(inputs_1)

    sym = SymmetryGenerator()
    variants_by_shape: dict[int, tuple[ShapeVariant, ...]] = {
        sid: sym.unique_variants(shape)
        for sid, shape in parsed.shapes.items()
    }

    pg = PlacementGenerator()
    solver = PackingSolver()

    placements_cache: dict[RegionKey, dict[int, tuple[Placement, ...]]] = {}

    fittable = 0
    for region in parsed.regions:
        key: RegionKey = (region.width, region.height)

        if key not in placements_cache:
            # placements depend only on region size + shape variants
            placements_cache[key] = pg.placements_by_shape(region, variants_by_shape)

        placements_by_shape = placements_cache[key]

        if solver.can_fit(
            region=region,
            required=region.required,
            shapes=parsed.shapes,
            placements_by_shape=placements_by_shape,
        ):
            fittable += 1

    return fittable


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    _ = inputs_1
    # Part 2 not specified in prompt excerpt
    return 0


if __name__ == "__main__":
    test = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
    print(f"Part 1: {solve_1(test)}")
    print(f"Part 2: {solve_2()}")
