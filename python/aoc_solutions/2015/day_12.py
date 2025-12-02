from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Optional
import json
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _parse_numbers(node: Any) -> Iterable[int]:
    """Visita ricorsivamente il JSON e restituisce tutti gli int trovati."""
    if isinstance(node, dict):
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from _parse_numbers(value)
            elif isinstance(value, int):
                yield value
    elif isinstance(node, list):
        for value in node:
            if isinstance(value, (dict, list)):
                yield from _parse_numbers(value)
            elif isinstance(value, int):
                yield value


def _parse_numbers_without_red(node: Any) -> Iterable[int]:
    """Come _parse_numbers, ma ignora gli oggetti che contengono 'red' come valore."""
    if isinstance(node, dict):
        if "red" in node.values():
            return
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from _parse_numbers_without_red(value)
            elif isinstance(value, int):
                yield value
    elif isinstance(node, list):
        for value in node:
            if isinstance(value, (dict, list)):
                yield from _parse_numbers_without_red(value)
            elif isinstance(value, int):
                yield value


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    data = json.loads(raw)
    return sum(_parse_numbers(data))


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    data = json.loads(raw)
    return sum(_parse_numbers_without_red(data))


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
