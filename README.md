# Advent of Code – Multi-language Playground (AoCv2)

Repository personale per risolvere gli esercizi di [Advent of Code](https://adventofcode.com/) usando più linguaggi:

- **Python** (con tooling per scaricare input e generare boilerplate)
- **Rust** (workspace con libreria condivisa)

L’obiettivo è avere:

- una **struttura dati unica** per tutte le soluzioni (`./data`)
- degli **strumenti comuni** (`./tools`) per scaricare input / testo
- una struttura ordinata per ogni linguaggio (`./python`, `./rust`, …)


## Struttura del repository

```text
.
├── data/                 # input e testo (instructions) di Advent of Code
├── tools/                # script di utilità (Python)
├── python/               # soluzioni Python + helper
└── rust/                 # workspace Rust (libreria + soluzioni per anno)
```

### `data/`

Gli input e il testo di ogni giorno stanno qui, condivisi da tutti i linguaggi:

```text
data/
└── {year}/
    └── day_{NN}/
        ├── input_1.txt
        └── instructions.md
```

Esempio: `data/2024/day_01/input_1.txt`

### `tools/`

Script Python che aiutano a preparare la giornata di lavoro:

* `get_day.py`
  Scarica **instructions** e **input** da Advent of Code per uno specifico anno/giorno.

* `new_python.py`
  Genera lo skeleton di un file Python per un certo anno/giorno:

  * assicura che gli input siano presenti (chiama `get_day.py`)
  * crea `python/aoc_solutions/{year}/day_{NN}.py` se non esiste.

* `new_rust.py`
  Genera lo skeleton di un binario Rust:

  * assicura che gli input siano presenti (chiama `get_day.py`)
  * crea (se serve) il crate `rust/crates/y{year}`
  * aggiunge il crate al workspace `rust/Cargo.toml`
  * crea `rust/crates/y{year}/src/bin/day_{NN}.rs` se non esiste.

### `python/`

Struttura prevista:

```text
python/
├── get_input.py              # classe GetInput per leggere i file di input
└── aoc_solutions/
    └── {year}/
        ├── day_01.py
        ├── day_02.py
        └── ...
```

Ogni `day_{NN}.py` usa la classe `GetInput` per trovare automaticamente l’input giusto in `./data`.

### `rust/`

Workspace Rust:

```text
rust/
├── Cargo.toml             # workspace (members = ["crates/aoclib", "crates/y{year}", ...])
└── crates/
    ├── aoclib/            # libreria condivisa per leggere gli input
    │   ├── Cargo.toml
    │   └── src/lib.rs
    └── y{year}/           # crate binario per l'anno {year}
        ├── Cargo.toml
        └── src/bin/
            ├── day_01.rs
            ├── day_02.rs
            └── ...
```

La libreria `aoclib` espone funzioni come:

* `read_input(year, day, part)` → legge `data/{year}/day_{NN}/input_{part}.txt`

---

## Requisiti

* **Python**: 3.11+ (testato con 3.12)
* **Rust**: toolchain stable (con `cargo`)
* Accesso ad un account **Advent of Code** (serve il cookie di sessione per scaricare gli input personali)

Python: dipendenze in `requirements.txt`:

```text
requests
beautifulsoup4
markdownify
python-dotenv
```

---

## Setup Python

### 1. Creare e attivare il virtualenv

Dalla **root del repo**:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 2. Installare le dipendenze

Con il venv attivo:

```bash
pip install -r requirements.txt
```

---

## Configurazione `AOC_SESSION`

Gli script in `tools/` usano il cookie di sessione di Advent of Code per scaricare gli input personali.

### 1. Recuperare il valore del cookie

1. Accedi a [https://adventofcode.com](https://adventofcode.com) dal browser.
2. Apri gli strumenti sviluppatore → sezione **Application / Storage / Cookies**.
3. Cerca il cookie chiamato `session`.
4. Copia **solo il valore**, una lunga stringa esadecimale (senza `session=` e senza `;` finali).

### 2. Opzione A – Variabile d’ambiente globale

Aggiungi al tuo `~/.bashrc` (o a un file custom che poi importi da lì):

```bash
export AOC_SESSION=il_tuo_cookie_lungo
```

Poi ricarica:

```bash
source ~/.bashrc
```

Verifica:

```bash
echo "$AOC_SESSION"
python -c "import os; print(os.getenv('AOC_SESSION'))"
```

---

## Script `tools/`

### `tools/get_day.py`

Scarica **testo** e **input** per un giorno specifico.

* Se **non passi argomenti** → usa **oggi** (`year` e `day` correnti).
* Se passi **solo -y o solo -d** → errore (vanno passati entrambi).
* Se passi **-y e -d** → usa quelli.

Salva i file in:

```text
data/{year}/day_{NN}/
    instructions.md
    input_1.txt
```

Esempi:

```bash
# giorno/anno correnti
./tools/get_day.py

# 1 dicembre 2024
./tools/get_day.py -y 2024 -d 1
```

Lo script è idempotente: se i file esistono già, li lascia stare e mostra `[SKIP]`.

### `tools/new_python.py`

Genera lo skeleton per una soluzione Python:

1. Assicura che `instructions.md` e `input_1.txt` per `year/day` esistano (riusa `get_day.py`).

2. Crea (se serve) la cartella:

   ```text
   python/aoc_solutions/{year}/
   ```

3. Crea il file:

   ```text
   python/aoc_solutions/{year}/day_{NN}.py
   ```

   se non esiste (se esiste → errore).

Dentro ci mette un template base che usa `GetInput`.

Esempi:

```bash
# oggi
./tools/new_python.py

# 5 dicembre 2024
./tools/new_python.py -y 2024 -d 5
```

### `tools/new_rust.py`

Genera lo skeleton per una soluzione Rust:

1. Assicura che `instructions.md` e `input_1.txt` per `year/day` esistano (riusa `get_day.py`).

2. Si aspetta che esista `rust/` con un workspace inizializzato e il crate `aoclib`.

3. Crea (se serve) il crate:

   ```text
   rust/crates/y{year}/
   ```

   con un `Cargo.toml` base che dipende da `aoclib`.

4. Aggiunge `crates/y{year}` alla lista `members` di `rust/Cargo.toml` (se manca).

5. Crea il file binario:

   ```text
   rust/crates/y{year}/src/bin/day_{NN}.rs
   ```

   se non esiste (se esiste → errore).

Esempi:

```bash
# oggi
./tools/new_rust.py

# 2 dicembre 2024
./tools/new_rust.py -y 2024 -d 2
```

---

## Soluzioni Python

### `python/get_input.py`

Contiene la classe `GetInput`, che:

* capisce **chi l’ha chiamata** (il file `day_{NN}.py`)

* inferisce:

  * `year` dalla cartella (`python/aoc_solutions/2024/day_01.py` → `2024`)
  * `day` dal nome file (`day_01.py` → `1`)

* costruisce il path:

  ```text
  data/{year}/day_{NN}/input_{part}.txt
  ```

* legge il file in `self.input` (stringa).

Uso tipico in un file `day_{NN}.py`:

```python
from __future__ import annotations

from pathlib import Path
import sys

# Rende importabile la classe GetInput dal folder python/
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()  # se serve, possiamo passare parametri (part, year, day, ...)


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    # TODO: implementare la logica della parte 1
    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string

    # TODO: implementare la logica della parte 2
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
```

### Eseguire una soluzione Python

Con il virtualenv attivo, dalla **root**:

```bash
cd python/aoc_solutions/2024
python day_01.py
```

Oppure puoi importare le funzioni `solve_1` / `solve_2` in test o script esterni.

---

## Soluzioni Rust

### Workspace

`rust/Cargo.toml` definisce il workspace:

```toml
[workspace]
members = [
    "crates/aoclib",
    "crates/y2024",
    # "crates/y2025", ...
]

resolver = "2"
```

### Libreria `aoclib`

In `rust/crates/aoclib/src/lib.rs` c’è la logica per trovare la root del repo e leggere gli input:

* se è impostata `AOC_ROOT`, usa quella come root del progetto;
* altrimenti risale le cartelle finché trova una directory con `data/`.

Funzione principale:

```rust
pub fn read_input(year: i32, day: u8, part: u8) -> std::io::Result<String>;
```

### Crate `y{year}`

Per ogni anno c’è un crate dedicato, es. `rust/crates/y2024/`.

Ogni giorno è un binario in `src/bin/day_{NN}.rs`, es.:

```rust
use aoclib::read_input;

const YEAR: i32 = 2024;
const DAY: u8 = 1;

fn part1(_input: &str) -> i64 {
    // TODO: implementa la logica della parte 1
    0
}

fn part2(_input: &str) -> i64 {
    // TODO: implementa la logica della parte 2
    0
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
```

### Eseguire una soluzione Rust

Dalla cartella `rust/`:

```bash
cargo run -p y2024 --bin day_01
```

Se necessario puoi impostare `AOC_ROOT` esplicitamente:

```bash
export AOC_ROOT=/percorso/assoluto/AoCv2
cargo run -p y2024 --bin day_01
```

---

## Note varie

* gli script in `tools/` sono pensati per essere **idempotenti**:

  * non sovrascrivono input / instructions esistenti
  * non sovrascrivono file di soluzioni esistenti (danno errore)
* la naming convention è:

  * giorni sempre con 2 cifre: `day_01`, `day_02`, …, `day_25`
  * cartella dati `day_{NN}` corrispondente sia per Python che per Rust
* il repository è pensato per essere esteso ad altri linguaggi
  (es. `./c`, `./haskell`, ecc.) riusando sempre `./data` come sorgente dati comune.

