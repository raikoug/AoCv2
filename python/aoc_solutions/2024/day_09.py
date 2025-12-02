from __future__ import annotations

from pathlib import Path
from typing import Optional

import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput  # type: ignore[import-untyped]


GI = GetInput()

Filesystem = list[str]


# --- Helpers comuni -------------------------------------------------------


def parse_disk_map(raw: str) -> tuple[list[int], list[int]]:
    """
    Parla la riga dell'input in:
    - file_lengths: lunghezze dei file (posizioni pari)
    - free_lengths: lunghezze degli spazi liberi (posizioni dispari)
    """
    digits = raw.strip()
    file_lengths = [int(ch) for ch in digits[::2]]
    free_lengths = [int(ch) for ch in digits[1::2]]
    return file_lengths, free_lengths


def build_filesystem(file_lengths: list[int], free_lengths: list[int]) -> Filesystem:
    """
    Costruisce il filesystem come lista di stringhe:
    - "id" per un blocco occupato dal file con id = indice
    - "." per uno spazio libero
    """
    filesystem: Filesystem = []
    for file_id, length in enumerate(file_lengths):
        # blocchi occupati dal file
        filesystem.extend(str(file_id) for _ in range(length))
        # blocchi liberi successivi (se presenti)
        if file_id < len(free_lengths):
            filesystem.extend("." for _ in range(free_lengths[file_id]))
    return filesystem


# --- Parte 1 --------------------------------------------------------------


def solve_1(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string

    file_lengths, free_lengths = parse_disk_map(inputs_1)
    filesystem = build_filesystem(file_lengths, free_lengths)

    # Compattazione naïve: spostiamo singoli blocchi da destra a sinistra
    end = False
    for i in range(len(filesystem) - 1, 0, -1):
        if filesystem[i] != ".":
            # cerca da sinistra il primo "." prima di i
            for j in range(i):
                if filesystem[j] == ".":
                    filesystem[i], filesystem[j] = filesystem[j], filesystem[i]
                    break
            else:
                # nessun movimento possibile: abbiamo finito
                end = True
        if end:
            break

    # Calcolo checksum: fermandosi al primo "."
    checksum = 0
    for idx, el in enumerate(filesystem):
        if el == ".":
            break
        checksum += idx * int(el)

    return checksum


# --- Parte 2 --------------------------------------------------------------


def solve_2(test_string: str | None = None) -> int:
    inputs_1: str = GI.input if test_string is None else test_string

    file_lengths, free_lengths = parse_disk_map(inputs_1)
    filesystem = build_filesystem(file_lengths, free_lengths)

    def get_file_start_end(fs: Filesystem, file_id: int) -> tuple[Optional[int], Optional[int]]:
        """
        Ritorna (start, end) del file con id file_id nel filesystem,
        oppure (None, None) se non trovato.
        """
        file_marker = str(file_id)
        try:
            start = fs.index(file_marker)
        except ValueError:
            return None, None  # file non presente
        length = file_lengths[file_id]
        end = start + length - 1
        return start, end

    def get_free_block_start(
        fs: Filesystem,
        block_length: int,
        max_pos: int,
    ) -> Optional[int]:
        """
        Cerca il primo blocco libero continuo di lunghezza block_length
        tra le posizioni [0, max_pos). Restituisce l'indice di inizio o None.
        """
        current_block_start: Optional[int] = None
        current_block_length = 0

        for idx in range(max_pos):
            if fs[idx] == ".":
                if current_block_start is None:
                    current_block_start = idx
                    current_block_length = 1
                else:
                    current_block_length += 1

                if current_block_length == block_length:
                    return current_block_start
            else:
                current_block_start = None
                current_block_length = 0

        return None

    max_file_id = len(file_lengths) - 1

    # Muoviamo i file interi da destra verso sinistra
    for fid in range(max_file_id, -1, -1):
        f_len = file_lengths[fid]
        if f_len == 0:
            continue

        start, end = get_file_start_end(filesystem, fid)
        if start is None or end is None:
            # File non presente (può capitare se l'abbiamo già mosso / eliminato)
            continue

        # Trova un blocco libero continuo della stessa lunghezza alla sinistra di start
        free_start = get_free_block_start(filesystem, f_len, start)
        if free_start is not None:
            # “Svuota” il file dalla posizione attuale
            for i in range(start, end + 1):
                filesystem[i] = "."
            # “Scrive” il file nella nuova posizione
            for i in range(f_len):
                filesystem[free_start + i] = str(fid)

    # Checksum: qui consideriamo tutti i blocchi occupati
    checksum = 0
    for idx, el in enumerate(filesystem):
        if el != ".":
            checksum += idx * int(el)

    return checksum


if __name__ == "__main__":
    test = "2333133121414131402"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
    # Per test:
    # print(f"Part 1 (test): {solve_1(test)}")
    # print(f"Part 2 (test): {solve_2(test)}")
