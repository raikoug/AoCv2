#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
import requests

import get_day  # riuso delle funzioni già scritte in tools/get_day.py


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crea un nuovo file Rust per un giorno di Advent of Code."
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
    with requests.Session() as session:
        # Cookie di sessione AoC
        session.cookies.set("session", token)
        session.headers.update(
            {"User-Agent": "AoC helper script (personal use)"}
        )

        get_day.download_instructions(session, year, day, day_dir)
        get_day.download_input(session, year, day, day_dir)

def ensure_workspace_member(rust_root: Path, member_path: str) -> None:
    """
    Assicura che `member_path` (es. "crates/y2024") sia presente
    nella lista `members = [ ... ]` di rust/Cargo.toml.
    Non fa parsing TOML serio: modifica solo la lista members come testo.
    """
    cargo_toml = rust_root / "Cargo.toml"
    if not cargo_toml.exists():
        print(f"[ERRORE] Non trovo {cargo_toml}. Inizializza prima il workspace Rust.", file=sys.stderr)
        sys.exit(1)

    text = cargo_toml.read_text(encoding="utf-8")
    target = f'"{member_path}"'

    if target in text:
        # già presente
        return

    lines = text.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if "members" in line and "[" in line:
            start_idx = i
            break

    if start_idx is None:
        print(
            "[WARN] Non ho trovato una sezione 'members = [ ... ]' in rust/Cargo.toml. "
            "Aggiungi il crate al workspace manualmente, se necessario.",
            file=sys.stderr,
        )
        return

    # trova la riga con ']'
    end_idx = start_idx + 1
    while end_idx < len(lines) and "]" not in lines[end_idx]:
        end_idx += 1

    if end_idx >= len(lines):
        print(
            "[WARN] Non sono riuscito a trovare la chiusura ']' per la lista members.",
            file=sys.stderr,
        )
        return

    # Inseriamo il nuovo membro prima della riga con ']'
    indent = "    "
    lines.insert(end_idx, f'{indent}{target},')

    new_text = "\n".join(lines) + "\n"
    cargo_toml.write_text(new_text, encoding="utf-8")
    print(f"[OK] Aggiunto {member_path} a rust/Cargo.toml")


def create_year_crate(rust_root: Path, year: int) -> Path:
    """
    Assicura che esista il crate rust/crates/y{year}/ con un Cargo.toml base.
    Non sovrascrive Cargo.toml se già esiste.
    Restituisce il path del crate.
    """
    crates_dir = rust_root / "crates"
    aoclib_dir = crates_dir / "aoclib"

    if not aoclib_dir.joinpath("Cargo.toml").exists():
        print(
            f"[ERRORE] Non trovo {aoclib_dir}/Cargo.toml. Inizializza prima il crate aoclib.",
            file=sys.stderr,
        )
        sys.exit(1)

    year_crate_dir = crates_dir / f"y{year}"
    year_crate_dir.mkdir(parents=True, exist_ok=True)

    cargo_toml = year_crate_dir / "Cargo.toml"
    if not cargo_toml.exists():
        cargo_content = f"""[package]
name = "y{year}"
version = "0.1.0"
edition = "2021"

[dependencies]
aoclib = {{ path = "../aoclib" }}
"""
        cargo_toml.write_text(cargo_content, encoding="utf-8")
        print(f"[OK] Creato {cargo_toml}")
    else:
        print(f"[INFO] {cargo_toml} esiste già, non lo modifico.")

    # assicuriamo che sia nel workspace
    ensure_workspace_member(rust_root, f"crates/y{year}")

    return year_crate_dir


def create_day_file(year_crate_dir: Path, year: int, day: int) -> None:
    """
    Crea src/bin/day_{NN}.rs per il crate dell'anno, se non esiste.
    """
    bin_dir = year_crate_dir / "src" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    day_file = bin_dir / f"day_{day:02d}.rs"
    if day_file.exists():
        print(f"[ERRORE] Il file {day_file} esiste già, non lo sovrascrivo.", file=sys.stderr)
        sys.exit(1)

    template = f"""use aoclib::read_input;

const YEAR: i32 = {year};
const DAY: u8 = {day};

fn part1(_input: &str) -> i64 {{
    // TODO: implementa la logica della parte 1
    0
}}

fn part2(_input: &str) -> i64 {{
    // TODO: implementa la logica della parte 2
    0
}}

fn main() {{
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {{}}", part1(&input));
    println!("Part 2: {{}}", part2(&input));
}}
"""
    day_file.write_text(template, encoding="utf-8")
    print(f"[OK] Creato {day_file}")


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

    # 2) Assicuriamoci che esista la cartella rust/
    rust_root = repo_root / "rust"
    if not rust_root.exists():
        print(f"[ERRORE] Non trovo la cartella {rust_root}. Creala e inizializza il workspace Rust.", file=sys.stderr)
        sys.exit(1)

    # 3) Assicuriamoci che esista il crate dell'anno (y{year}) con Cargo.toml
    year_crate_dir = create_year_crate(rust_root, year)

    # 4) Creiamo il file src/bin/day_{NN}.rs per quell'anno
    create_day_file(year_crate_dir, year, day)


if __name__ == "__main__":
    main()
