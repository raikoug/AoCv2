#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NIM_DIR = ROOT / "nim"
AOCLIB_DIR = NIM_DIR / "aoclib"
SOLUTIONS_ROOT = NIM_DIR / "aoc_solutions"

AOC_INPUT_NIM = """import std/[os, strformat, strutils]

proc readInput*(year: int; day: int; part: int = 1): string =
  ## Legge l'input AoC da data/{year}/day_{NN}/input_{part}.txt
  ##
  ## Esempio:
  ##   let s = readInput(2016, 1)  # data/2016/day_01/input_1.txt
  let nn = &"{day:02}"
  let path = &"data/{year}/day_{nn}/input_{part}.txt"
  result = readFile(path)

proc readLines*(year: int; day: int; part: int = 1): seq[string] =
  ## Ritorna le righe come seq[string]
  readInput(year, day, part).splitLines()
"""



def day_template(year: int, day: int) -> str:
    return f"""import std/strutils
import aoclib/aoc_input

const
  Year* = {year}
  Day*  = {day}

proc part1*(input: string): string =

  discard
  result = ""

proc part2*(input: string): string =

  discard
  result = ""

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
"""


def ensure_aoclib() -> None:
    AOCLIB_DIR.mkdir(parents=True, exist_ok=True)
    aoc_input_path = AOCLIB_DIR / "aoc_input.nim"
    if not aoc_input_path.exists():
        aoc_input_path.write_text(AOC_INPUT_NIM)
        print(f"[new_nim] Created {aoc_input_path.relative_to(ROOT)}")
    else:
        print(f"[new_nim] {aoc_input_path.relative_to(ROOT)} already exists")


def create_day(year: int, day: int) -> None:
    if not (1 <= day <= 25):
        raise SystemExit("day must be between 1 and 25")

    NIM_DIR.mkdir(exist_ok=True)
    ensure_aoclib()

    year_dir = SOLUTIONS_ROOT / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)

    day_filename = f"day_{day:02}.nim"
    day_path = year_dir / day_filename

    if day_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {day_path}")

    day_path.write_text(day_template(year, day))
    print(f"[new_nim] Created {day_path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Nim AoC skeleton")
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    args = parser.parse_args()

    create_day(args.year, args.day)


if __name__ == "__main__":
    main()
