from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
import time
from collections import OrderedDict
from multiprocessing import get_context
from typing import Callable, ClassVar, Final, TypeAlias

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


# -----------------------------
# Lazy input loading (worker-safe)
# -----------------------------
GI: GetInput | None = None


def load_input(test_string: str | None) -> str:
    if test_string is not None:
        return test_string
    global GI
    if GI is None:
        GI = GetInput()
    return GI.input


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

RequiredItems: TypeAlias = tuple[tuple[int, int], ...]  # picklable compact required
MaskTuple: TypeAlias = tuple[Mask, ...]
MasksByShape: TypeAlias = dict[int, MaskTuple]

AreaFn: TypeAlias = Callable[[int, int], int]
area: AreaFn = lambda w, h: w * h

ToIntFn: TypeAlias = Callable[[str], int]
to_int: ToIntFn = lambda s: int(s)

SetBitFn: TypeAlias = Callable[[Mask, int], Mask]
set_bit: SetBitFn = lambda mask, idx: mask | (1 << idx)

NowFn: TypeAlias = Callable[[], float]
now: NowFn = lambda: time.monotonic()


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
# Placements (point 3, memory-optimized)
# -----------------------------
@dataclass(frozen=True, slots=True)
class PlacementGenerator:
    """
    Returns ONLY masks (tuple[int,...]) per shape for given region size.
    placement_id == index in the tuple (stable ordering).
    """

    def masks_by_shape(
        self,
        width: int,
        height: int,
        variants_by_shape: dict[int, tuple[ShapeVariant, ...]],
    ) -> MasksByShape:
        out: MasksByShape = {}
        W = width
        H = height

        for shape_id, variants in variants_by_shape.items():
            masks: list[Mask] = []
            for variant in variants:
                masks.extend(self._masks_for_variant(W, H, variant))
            out[shape_id] = tuple(masks)

        return out

    def _masks_for_variant(self, W: int, H: int, variant: ShapeVariant) -> list[Mask]:
        if variant.width > W or variant.height > H:
            return []

        masks: list[Mask] = []
        max_dx = W - variant.width
        max_dy = H - variant.height

        for dy in range(max_dy + 1):
            row_base = (dy * W)
            for dx in range(max_dx + 1):
                base = row_base + dx
                mask: Mask = 0
                for (x, y) in variant.cells:
                    idx = base + (y * W) + x
                    mask = set_bit(mask, idx)
                masks.append(mask)

        return masks


# -----------------------------
# Solver (point 4)
# -----------------------------
@dataclass(frozen=True, slots=True)
class PackingContext:
    shapes: dict[int, Shape]
    shape_area: dict[int, int]


@dataclass(frozen=True, slots=True)
class PackingSolver:
    def can_fit(
        self,
        region: RegionSpec,
        context: PackingContext,
        placements_by_shape: MasksByShape,
    ) -> bool:
        region_area = region.region_area
        remaining_counts: dict[int, int] = dict(region.required)

        remaining_area = self._required_area(remaining_counts, context.shape_area)
        if remaining_area > region_area:
            return False

        for sid, qty in remaining_counts.items():
            if qty <= 0:
                continue
            masks = placements_by_shape.get(sid)
            if masks is None or len(masks) == 0:
                return False

        used: Mask = 0
        min_pid_by_shape: dict[int, int] = {}

        return self._dfs(
            used=used,
            remaining_counts=remaining_counts,
            remaining_area=remaining_area,
            region_area=region_area,
            placements_by_shape=placements_by_shape,
            shape_area=context.shape_area,
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
        placements_by_shape: MasksByShape,
        shape_area: dict[int, int],
        min_pid_by_shape: dict[int, int],
    ) -> bool:
        if remaining_area == 0:
            return True

        free_cells = region_area - used.bit_count()
        if remaining_area > free_cells:
            return False

        chosen_sid: int | None = None
        chosen_candidates: list[int] = []
        best_n: int | None = None

        for sid, qty in remaining_counts.items():
            if qty <= 0:
                continue

            masks = placements_by_shape[sid]
            start_pid = min_pid_by_shape.get(sid, 0)

            candidates: list[int] = []
            for pid in range(start_pid, len(masks)):
                m = masks[pid]
                if (used & m) == 0:
                    candidates.append(pid)

            n = len(candidates)
            if n == 0:
                return False

            if best_n is None or n < best_n:
                best_n = n
                chosen_sid = sid
                chosen_candidates = candidates
                if best_n == 1:
                    break

        if chosen_sid is None:
            return False

        sid = chosen_sid
        old_qty = remaining_counts[sid]
        old_min_present = sid in min_pid_by_shape
        old_min = min_pid_by_shape.get(sid, 0)

        masks = placements_by_shape[sid]
        piece_area = shape_area[sid]

        for pid in chosen_candidates:
            m = masks[pid]

            remaining_counts[sid] = old_qty - 1
            min_pid_by_shape[sid] = pid + 1

            if self._dfs(
                used=used | m,
                remaining_counts=remaining_counts,
                remaining_area=remaining_area - piece_area,
                region_area=region_area,
                placements_by_shape=placements_by_shape,
                shape_area=shape_area,
                min_pid_by_shape=min_pid_by_shape,
            ):
                return True

            remaining_counts[sid] = old_qty
            if old_min_present:
                min_pid_by_shape[sid] = old_min
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
        lines = raw.strip("\n").splitlines()

        region_start = self._find_first_region_line(lines)
        shape_lines = lines[:region_start]
        region_lines = lines[region_start:]

        shapes = self._parse_shapes(shape_lines)
        if not shapes:
            raise ValueError("No shapes found in input.")

        shape_order = tuple(sorted(shapes.keys()))
        regions = self._parse_regions(region_lines, shape_order)

        return ParsedInput(shapes=shapes, shape_order=shape_order, regions=regions)

    def _find_first_region_line(self, lines: list[str]) -> int:
        for i, ln in enumerate(lines):
            if self.REGION_RE.match(ln) is not None:
                return i
        raise ValueError("Could not find any region lines (e.g. '12x5: ...') in input.")

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
# Parallel execution + progress
# -----------------------------
@dataclass(frozen=True, slots=True)
class RegionTask:
    width: int
    height: int
    required_items: RequiredItems
    raw_line: str


@dataclass(slots=True)
class ProgressPrinter:
    total: int
    bar_width: int = 28
    min_interval_s: float = 0.20

    start_t: float = 0.0
    last_t: float = 0.0

    def start(self) -> None:
        t = now()
        self.start_t = t
        self.last_t = t
        self.render(done=0, ok=0, force=True)

    def render(self, done: int, ok: int, force: bool = False) -> None:
        t = now()
        if (not force) and (t - self.last_t) < self.min_interval_s and done < self.total:
            return
        self.last_t = t

        frac = 1.0 if self.total == 0 else (done / self.total)
        fill = int(self.bar_width * frac)
        bar = ("#" * fill) + ("." * (self.bar_width - fill))

        elapsed = max(1e-9, t - self.start_t)
        rate = done / elapsed

        msg = f"\r[{bar}] {done}/{self.total}  ok={ok}  {rate:.1f}/s"
        print(msg, end="", flush=True)

        if done == self.total:
            print("", flush=True)  # newline


# Worker globals (set by initializer)
_W_CONTEXT: PackingContext | None = None
_W_VARIANTS: dict[int, tuple[ShapeVariant, ...]] | None = None
_W_SOLVER: PackingSolver | None = None
_W_PG: PlacementGenerator | None = None
_W_CACHE: OrderedDict[RegionKey, MasksByShape] | None = None
_W_CACHE_MAX: int = 0


def _init_worker(
    context: PackingContext,
    variants_by_shape: dict[int, tuple[ShapeVariant, ...]],
    cache_max_sizes: int,
) -> None:
    global _W_CONTEXT, _W_VARIANTS, _W_SOLVER, _W_PG, _W_CACHE, _W_CACHE_MAX
    _W_CONTEXT = context
    _W_VARIANTS = variants_by_shape
    _W_SOLVER = PackingSolver()
    _W_PG = PlacementGenerator()
    _W_CACHE = OrderedDict()
    _W_CACHE_MAX = cache_max_sizes


def _get_masks_for_size(key: RegionKey) -> MasksByShape:
    assert _W_CACHE is not None
    assert _W_PG is not None
    assert _W_VARIANTS is not None

    if key in _W_CACHE:
        _W_CACHE.move_to_end(key)
        return _W_CACHE[key]

    w, h = key
    masks = _W_PG.masks_by_shape(w, h, _W_VARIANTS)

    _W_CACHE[key] = masks
    _W_CACHE.move_to_end(key)

    if _W_CACHE_MAX > 0 and len(_W_CACHE) > _W_CACHE_MAX:
        _W_CACHE.popitem(last=False)

    return masks


def _solve_region_task(task: RegionTask) -> bool:
    assert _W_CONTEXT is not None
    assert _W_SOLVER is not None

    required = dict(task.required_items)
    region = RegionSpec(width=task.width, height=task.height, required=required, raw_line=task.raw_line)

    masks_by_shape = _get_masks_for_size((task.width, task.height))

    return _W_SOLVER.can_fit(region=region, context=_W_CONTEXT, placements_by_shape=masks_by_shape)


@dataclass(frozen=True, slots=True)
class ParallelRegionChecker:
    workers: int
    chunksize: int
    cache_max_sizes_per_worker: int = 8  # LRU max distinct (W,H) per process

    def count_fittable(
        self,
        tasks: list[RegionTask],
        context: PackingContext,
        variants_by_shape: dict[int, tuple[ShapeVariant, ...]],
        show_progress: bool = True,
    ) -> int:
        if not tasks:
            return 0

        # "fork" on Linux is fast; fallback to default context
        ctx = get_context()

        total = len(tasks)
        ok = 0
        done = 0

        pp = ProgressPrinter(total=total)
        if show_progress:
            pp.start()

        with ctx.Pool(
            processes=self.workers,
            initializer=_init_worker,
            initargs=(context, variants_by_shape, self.cache_max_sizes_per_worker),
        ) as pool:
            for res in pool.imap_unordered(_solve_region_task, tasks, chunksize=self.chunksize):
                done += 1
                if res:
                    ok += 1
                if show_progress:
                    pp.render(done=done, ok=ok, force=(done == total))

        return ok


# -----------------------------
# Solutions
# -----------------------------
def solve_1(test_string: str | None = None) -> int:
    inputs_1 = load_input(test_string)

    parsed = InputParser().parse(inputs_1)

    sym = SymmetryGenerator()
    variants_by_shape: dict[int, tuple[ShapeVariant, ...]] = {
        sid: sym.unique_variants(shape)
        for sid, shape in parsed.shapes.items()
    }

    context = PackingContext(
        shapes=parsed.shapes,
        shape_area={sid: s.filled_area for sid, s in parsed.shapes.items()},
    )

    tasks: list[RegionTask] = [
        RegionTask(
            width=r.width,
            height=r.height,
            required_items=tuple(sorted(r.required.items())),
            raw_line=r.raw_line,
        )
        for r in parsed.regions
    ]

    # full throttle
    cpu = max(1, len(get_context().cpu_count().__class__.__mro__) and 1)  # avoid mypy noise
    workers = get_context().cpu_count()  # type: ignore[attr-defined]

    workers = max(1, min(workers, len(tasks)))
    chunksize = max(1, len(tasks) // (workers * 8))

    checker = ParallelRegionChecker(
        workers=workers,
        chunksize=chunksize,
        cache_max_sizes_per_worker=8,
    )

    return checker.count_fittable(
        tasks=tasks,
        context=context,
        variants_by_shape=variants_by_shape,
        show_progress=True,
    )


def solve_2(test_string: str | None = None) -> int:
    _ = load_input(test_string)
    # Part 2 not specified in prompt excerpt
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
