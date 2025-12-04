#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import requests
import get_day

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new Nim file for an Advent of Code day."
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year (e.g. 2024)",
    )
    parser.add_argument(
        "-d",
        "--day",
        type=int,
        help="Day (1-25)",
    )

    args = parser.parse_args()

    # If exactly one of the two is provided → error (XOR)
    if (args.year is None) ^ (args.day is None):
        parser.error("You must specify *both* -y/--year and -d/--day, or neither.")

    # No args → use today's year/day
    if args.year is None and args.day is None:
        today = date.today()
        args.year = today.year
        args.day = today.day

    return args


def ensure_day_data(repo_root: Path, year: int, day: int) -> None:
    """
    Use tools/get_day.py helpers to ensure instructions.md and input_1.txt
    exist for the given year/day.
    """
    # AoC session token
    token = get_day.get_session_token()

    # Create data/{year}/day_{NN} directory
    day_dir = get_day.ensure_day_dir(repo_root, year, day)

    # Download instructions and input (idempotent: SKIP if they already exist)
    with requests.Session() as session:
        # AoC session cookie
        session.cookies.set("session", token)
        session.headers.update(
            {"User-Agent": "AoC helper script (new_nim.py, personal use)"}
        )

        get_day.download_instructions(session, year, day, day_dir)
        get_day.download_input(session, year, day, day_dir)


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
        print(
            f"[WARN] Suspicious day: {day}. Advent of Code usually runs from 1 to 25.",
            file=sys.stderr,
        )

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
    repo_root = ROOT

    args = parse_args()
    year: int = args.year
    day: int = args.day

    # 1) Ensure instructions & input_1 exist (same behavior as new_python.py)
    ensure_day_data(repo_root, year, day)

    # 2) Create Nim day file
    create_day(year, day)


if __name__ == "__main__":
    main()
