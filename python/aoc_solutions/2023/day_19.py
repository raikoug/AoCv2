from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Tuple, List
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]

GI = GetInput()


Rating = Dict[str, int]
Interval = Dict[str, tuple[int, int]]  # inclusive ranges for x, m, a, s


def _parse_input(raw: str) -> tuple[dict[str, list[str]], list[Rating]]:
    workflows_raw, parts_raw = raw.strip().split("\n\n")

    workflows: dict[str, list[str]] = {}
    for line in workflows_raw.splitlines():
        name, rest = line.split("{", 1)
        rules_str = rest.rstrip("}")
        # es: "x<2006:qkq,m>2090:A,rfg"
        workflows[name] = rules_str.split(",")

    parts: list[Rating] = []
    for line in parts_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # {x=787,m=2655,a=1222,s=2876}
        inner = line.strip("{}")
        fields = inner.split(",")
        rating: Rating = {}
        for f in fields:
            k, v = f.split("=")
            rating[k] = int(v)
        parts.append(rating)

    return workflows, parts


def _eval_workflow(workflows: dict[str, list[str]], rating: Rating) -> str:
    current = "in"
    while True:
        rules = workflows[current]
        for rule in rules:
            if ":" in rule:
                cond, dest = rule.split(":")
                var = cond[0]
                op = cond[1]
                threshold = int(cond[2:])
                val = rating[var]
                ok = (val < threshold) if op == "<" else (val > threshold)
                if ok:
                    current = dest
                    break
            else:
                # default
                current = rule
                break
        if current in ("A", "R"):
            return current


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    workflows, parts = _parse_input(raw)
    total = 0
    for rating in parts:
        res = _eval_workflow(workflows, rating)
        if res == "A":
            total += sum(rating.values())
    return total


def _count_accepted(workflows: dict[str, list[str]]) -> int:
    # DFS sugli intervalli
    start_intervals: Interval = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }

    def split_interval(
        intervals: Interval,
        var: str,
        op: str,
        threshold: int,
    ) -> tuple[Optional[Interval], Optional[Interval]]:
        lo, hi = intervals[var]
        if op == "<":
            # true: [lo, threshold-1]
            t_hi = min(hi, threshold - 1)
            f_lo = max(lo, threshold)
            true_iv: Optional[Interval] = None
            false_iv: Optional[Interval] = None
            if lo <= t_hi:
                true_iv = dict(intervals)
                true_iv[var] = (lo, t_hi)
            if f_lo <= hi:
                false_iv = dict(intervals)
                false_iv[var] = (f_lo, hi)
            return true_iv, false_iv
        else:
            # op == '>' => true: [threshold+1, hi]
            t_lo = max(lo, threshold + 1)
            f_hi = min(hi, threshold)
            true_iv = None
            false_iv = None
            if t_lo <= hi:
                true_iv = dict(intervals)
                true_iv[var] = (t_lo, hi)
            if lo <= f_hi:
                false_iv = dict(intervals)
                false_iv[var] = (lo, f_hi)
            return true_iv, false_iv

    def count_interval(iv: Interval) -> int:
        prod = 1
        for lo, hi in iv.values():
            prod *= hi - lo + 1
        return prod

    total = 0
    stack: list[tuple[str, Interval]] = [("in", start_intervals)]

    while stack:
        wf_name, iv = stack.pop()
        if wf_name == "R":
            continue
        if wf_name == "A":
            total += count_interval(iv)
            continue

        rules = workflows[wf_name]
        current_intervals = iv
        for rule in rules:
            if ":" in rule:
                cond, dest = rule.split(":")
                var = cond[0]
                op = cond[1]
                threshold = int(cond[2:])
                true_iv, false_iv = split_interval(current_intervals, var, op, threshold)
                if true_iv is not None:
                    stack.append((dest, true_iv))
                if false_iv is None:
                    current_intervals = None
                    break
                current_intervals = false_iv
            else:
                # destinazione di default
                if current_intervals is not None:
                    stack.append((rule, current_intervals))
                current_intervals = None
                break

    return total


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    workflows, _ = _parse_input(raw)
    return _count_accepted(workflows)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
