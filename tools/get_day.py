#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scarica input e testo di un giorno di Advent of Code."
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



def get_session_token() -> str:
    token = os.getenv("AOC_SESSION")
    if not token:
        print(
            "Errore: variabile d'ambiente AOC_SESSION non impostata.\n"
            "Imposta AOC_SESSION o crea un file .env con ad es.:\n"
            "AOC_SESSION=il_tuo_cookie_di_sessione_di_adventofcode",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def ensure_day_dir(root: Path, year: int, day: int) -> Path:
    day_dir = root / "data" / str(year) / f"day_{day:02d}"
    day_dir.mkdir(parents=True, exist_ok=True)
    return day_dir


def download_instructions(session: requests.Session, year: int, day: int, day_dir: Path) -> None:
    instr_path = day_dir / "instructions.md"
    if instr_path.exists():
        print(f"[SKIP] {instr_path} esiste già.")
        return

    url = f"https://adventofcode.com/{year}/day/{day}"
    print(f"[GET] {url}")
    resp = session.get(url)
    if not resp.ok:
        print(
            f"[ERRORE] Impossibile scaricare instructions (HTTP {resp.status_code}) da {url}",
            file=sys.stderr,
        )
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.find_all("article", class_="day-desc")
    if not articles:
        print(
            "[WARN] Nessun <article class='day-desc'> trovato nella pagina.",
            file=sys.stderr,
        )
        return

    parts = [md(a.decode_contents()) for a in articles]
    content = "\n\n".join(parts)

    instr_path.write_text(content, encoding="utf-8")
    print(f"[OK] Scritto {instr_path}")


def download_input(session: requests.Session, year: int, day: int, day_dir: Path) -> None:
    input_path = day_dir / "input_1.txt"
    if input_path.exists():
        print(f"[SKIP] {input_path} esiste già.")
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    print(f"[GET] {url}")
    resp = session.get(url)
    if not resp.ok:
        print(
            f"[ERRORE] Impossibile scaricare input (HTTP {resp.status_code}) da {url}",
            file=sys.stderr,
        )
        return

    # Mantengo una newline finale
    text = resp.text
    if not text.endswith("\n"):
        text += "\n"

    input_path.write_text(text, encoding="utf-8")
    print(f"[OK] Scritto {input_path}")


def main() -> None:
    # Root del repo: un livello sopra tools/
    repo_root = Path(__file__).resolve().parent.parent

    # Argomenti
    args = parse_args()
    year = args.year
    day = args.day

    if not (1 <= day <= 25):
        print(
            f"[WARN] Giorno sospetto: {day}. Advent of Code va tipicamente da 1 a 25.",
            file=sys.stderr,
        )

    token = get_session_token()

    day_dir = ensure_day_dir(repo_root, year, day)

    with requests.Session() as session:
        # Cookie di sessione AoC
        session.cookies.set("session", token)
        session.headers.update(
            {"User-Agent": "AoC helper script (personal use)"}
        )

        download_instructions(session, year, day, day_dir)
        download_input(session, year, day, day_dir)


if __name__ == "__main__":
    main()
