# python/get_input.py
from __future__ import annotations

import inspect
from pathlib import Path
from typing import Optional


class GetInput:
    """
    Helper per caricare l'input di Advent of Code.

    Convenzione attesa per il file chiamante:
        ./python/aoc_solutions/{year}/day_{NN}.py

    Convenzione per i dati:
        ./data/{year}/day_{NN}/input_{part}.txt
    """
    input: str
    input_lines: list

    def __init__(
        self,
        *,
        part: int = 1,
        year: Optional[int] = None,
        day: Optional[int] = None,
        root: Optional[Path] = None,
    ) -> None:
        # Chi mi ha chiamato? (file day_XX.py)
        stack = inspect.stack()
        # 0 = questo __init__
        # 1 = punto dove è stato fatto GetInput()
        caller_frame = stack[1]
        caller_file = Path(caller_frame.filename).resolve()
        self.caller_file = caller_file

        # Se year non è passato, provo a inferirlo dalla cartella
        if year is None:
            parent_name = caller_file.parent.name  # es. "2024"
            try:
                year = int(parent_name)
            except ValueError as exc:
                raise ValueError(
                    f"Impossibile inferire l'anno dalla cartella '{parent_name}'. "
                    "Passa 'year=' esplicitamente a GetInput(...)."
                ) from exc

        # Se day non è passato, provo a inferirlo dal nome file
        if day is None:
            stem = caller_file.stem  # es. "day_01"
            prefix = "day_"
            if stem.startswith(prefix):
                num_str = stem[len(prefix) :]
                try:
                    day = int(num_str)
                except ValueError as exc:
                    raise ValueError(
                        f"Impossibile inferire il giorno dal nome file '{stem}'. "
                        "Atteso qualcosa tipo 'day_01.py'."
                    ) from exc
            else:
                raise ValueError(
                    f"Impossibile inferire il giorno dal nome file '{stem}'. "
                    "Atteso qualcosa tipo 'day_01.py'."
                )

        self.year: int = year
        self.day: int = day
        self.part: int = part

        # Root del repo: assumo che questo file sia in ./python/get_input.py
        # quindi repo_root è il parent della cartella python.
        if root is None:
            root = Path(__file__).resolve().parent.parent
        self.root: Path = root

        # Path dell'input
        self.path: Path = (
            self.root
            / "data"
            / str(self.year)
            / f"day_{self.day:02d}"
            / f"input_{self.part}.txt"
        )

        if not self.path.exists():
            raise FileNotFoundError(
                f"File di input non trovato: {self.path}\n"
                "Hai già lanciato tools/get_day.py per questo giorno?"
            )

        # Contenuto effettivo dell'input
        self.input: str = self.path.read_text(encoding="utf-8")
        self.input_list : list = self.input.splitlines()

