from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()


def _hash_label(label: str) -> int:
    """
    Funzione di hash definita nel problema:
    per ogni carattere:
      - aggiungi il suo codice ASCII
      - moltiplica per 17
      - prendi modulo 256
    """
    value = 0
    for ch in label:
        value += ord(ch)
        value *= 17
        value %= 256
    return value


@dataclass
class Lens:
    label: str
    focal_length: int


def _parse_steps(raw: str) -> List[str]:
    return [step for step in raw.replace("\n", "").split(",") if step]


def solve_1(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    steps = _parse_steps(raw)
    return sum(_hash_label(step) for step in steps)


def solve_2(test_string: Optional[str] = None) -> int:
    raw = GI.input if test_string is None else test_string
    steps = _parse_steps(raw)

    # boxes[box_index] -> lista di lenti nell'ordine corrente
    boxes: Dict[int, List[Lens]] = {i: [] for i in range(256)}

    for step in steps:
        if step.endswith("-"):
            label = step[:-1]
            box_index = _hash_label(label)
            box = boxes[box_index]
            boxes[box_index] = [lens for lens in box if lens.label != label]
        else:
            label, focal_str = step.split("=")
            focal = int(focal_str)
            box_index = _hash_label(label)
            box = boxes[box_index]

            for lens in box:
                if lens.label == label:
                    lens.focal_length = focal
                    break
            else:
                box.append(Lens(label=label, focal_length=focal))

    focusing_power = 0
    for box_index, box in boxes.items():
        for slot_index, lens in enumerate(box):
            focusing_power += (box_index + 1) * (slot_index + 1) * lens.focal_length

    return focusing_power


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
