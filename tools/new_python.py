#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
import requests

import get_day  

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crea un nuovo file Python per un giorno di Advent of Code."
    )
    parser.add_argument(
        "-y", "--year",
        type=int,
        help="Anno (es. 2024)"
    )
    parser.add_argument(
        "-d", "--day",
        type=int,
        help="Giorno (1-25)"
    )

    args = parser.parse_args()

    # Se uno solo dei due è presente → errore
    if (args.year is None) ^ (args.day is None):  # XOR
        parser.error("Devi specificare *entrambi* -y/--year e -d/--day, oppure nessuno.")

    # Nessun argomento → usa oggi
    if args.year is None and args.day is None:
        today = date.today()
        args.year = today.year
        args.day = today.day

    return args


def ensure_day_data(repo_root: Path, year: int, day: int) -> None:
    """
    Usa le funzioni di tools/get_day.py per assicurarsi che
    instructions.md e input_1.txt esistano per year/day.
    """

    # Token di sessione AoC
    token = get_day.get_session_token()

    # Crea la cartella data/{year}/day_{NN}
    day_dir = get_day.ensure_day_dir(repo_root, year, day)

    # Scarica instructions e input (idempotente: se esistono, fa SKIP)

    with requests.Session() as session:
        # Cookie di sessione AoC
        session.cookies.set("session", token)
        session.headers.update(
            {"User-Agent": "AoC helper script (personal use)"}
        )

        get_day.download_instructions(session, year, day, day_dir)
        get_day.download_input(session, year, day, day_dir)



TEMPLATE = '''from __future__ import annotations

from pathlib import Path
import sys

PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    
    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
'''


def main() -> None:
    # Root del repo: un livello sopra tools/
    repo_root = Path(__file__).resolve().parent.parent

    args = parse_args()
    year = args.year
    day = args.day

    if not (1 <= day <= 25):
        print(
            f"[WARN] Giorno sospetto: {day}. Advent of Code va tipicamente da 1 a 25.",
            file=sys.stderr,
        )

    # 1) Assicuriamoci che esistano instructions & input_1
    ensure_day_data(repo_root, year, day)

    # 2) Creiamo la cartella ./python/aoc_solutions/{year}/ se non esiste
    solutions_dir = repo_root / "python" / "aoc_solutions" / str(year)
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # 3) Creiamo il file day_{NN}.py
    day_file = solutions_dir / f"day_{day:02d}.py"
    if day_file.exists():
        print(f"[ERRORE] Il file {day_file} esiste già, non lo sovrascrivo.", file=sys.stderr)
        sys.exit(1)

    day_file.write_text(TEMPLATE, encoding="utf-8")
    print(f"[OK] Creato {day_file}")


if __name__ == "__main__":
    main()
