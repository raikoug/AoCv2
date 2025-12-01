# Advent of Code – Multi-language Playground (AoCv2)

Personal repository for solving [Advent of Code](https://adventofcode.com/) exercises using multiple languages:

- **Python** (with tooling to download inputs and generate boilerplate)
- **Rust** (workspace with a shared library)
- **Nim** (lightweight compiled solutions with their own helper module)

The goals:

- a **single data source** for all solutions (`./data`)
- **common tooling** (`./tools`) to download inputs / puzzle text
- a clean per-language structure (`./python`, `./rust`, `./nim`, …)


## Repository structure

```text
.
├── data/                 # Advent of Code inputs and (optionally) instructions
├── tools/                # utility scripts (Python)
├── python/               # Python solutions + helpers
├── rust/                 # Rust workspace (shared lib + per-year crates)
└── nim/                  # Nim helpers + per-year solutions
```

### `data/`

Inputs and (optionally) puzzle text for each day live here, shared by all languages:

```text
data/
└── {year}/
    └── day_{NN}/
        ├── input_1.txt
        └── instructions.md
```

Example: `data/2024/day_01/input_1.txt`


### `tools/`

Python scripts that help prepare each day:

- `get_day.py`  
  Downloads **instructions** and **input** from Advent of Code for a given year/day.

- `new_python.py`  
  Generates a Python solution skeleton for a given year/day:

  - ensures inputs exist (calls `get_day.py`)
  - creates `python/aoc_solutions/{year}/day_{NN}.py` if it does not exist.

- `new_rust.py`  
  Generates a Rust solution skeleton:

  - ensures inputs exist (calls `get_day.py`)
  - creates (if needed) the crate `rust/crates/y{year}`
  - adds the crate to the workspace `rust/Cargo.toml`
  - creates `rust/crates/y{year}/src/bin/day_{NN}.rs` if it does not exist.

- `new_nim.py`  
  Generates a Nim solution skeleton:

  - (current behavior) ensures `nim/aoclib/aoc_input.nim` exists
  - creates `nim/aoc_solutions/{year}/day_{NN}.nim` if it does not exist

  At the moment `new_nim.py` does **not** automatically call `get_day.py`, so you may want to fetch the input first with `tools/get_day.py`.


### `python/`

Expected structure:

```text
python/
├── get_input.py              # GetInput class to read AoC input files
└── aoc_solutions/
    └── {year}/
        ├── day_01.py
        ├── day_02.py
        └── ...
```

Each `day_{NN}.py` uses the `GetInput` class to locate the correct input file under `./data`.

Typical usage inside a `day_{NN}.py`:

```python
from __future__ import annotations

from pathlib import Path
import sys

# Make GetInput importable from the python/ folder
PYTHON_DIR = Path(__file__).resolve().parents[2]
if str(PYTHON_DIR) not in sys.path:
    sys.path.append(str(PYTHON_DIR))

from get_input import GetInput


GI = GetInput()  # you can optionally pass params (part, year, day, ...)


def solve_1(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    # TODO: implement part 1
    return 0


def solve_2(test_string: str | None = None) -> int:
    inputs_1 = GI.input if test_string is None else test_string
    # TODO: implement part 2
    return 0


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
```

To run a Python solution (from repo root, with venv active):

```bash
cd python/aoc_solutions/2024
python day_01.py
```


### `rust/`

Rust workspace:

```text
rust/
├── Cargo.toml             # workspace (members = ["crates/aoclib", "crates/y{year}", ...])
└── crates/
    ├── aoclib/            # shared library to read inputs
    │   ├── Cargo.toml
    │   └── src/lib.rs
    └── y{year}/           # binary crate for year {year}
        ├── Cargo.toml
        └── src/bin/
            ├── day_01.rs
            ├── day_02.rs
            └── ...
```

The `aoclib` library exposes functions such as:

- `read_input(year, day, part)` → reads `data/{year}/day_{NN}/input_{part}.txt`

Example structure for a single day:

```rust
use aoclib::read_input;

const YEAR: i32 = 2024;
const DAY: u8 = 1;

fn part1(_input: &str) -> i64 {
    // TODO
    0
}

fn part2(_input: &str) -> i64 {
    // TODO
    0
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
```

Run a Rust solution from `rust/`:

```bash
cd rust
cargo run -p y2024 --bin day_01
```

You can optionally set `AOC_ROOT` to point explicitly to the repo root:

```bash
export AOC_ROOT=/absolute/path/to/AoCv2
cargo run -p y2024 --bin day_01
```


### `nim/`

Nim helpers and per-year solutions.

```text
nim/
├── nim.cfg                 # config so Nim finds aoclib/ when linting/compiling
├── aoclib/
│   └── aoc_input.nim       # helper to read AoC input files from ../data
└── aoc_solutions/
    └── {year}/
        ├── day_01.nim
        ├── day_02.nim
        └── ...
```

#### `nim/aoclib/aoc_input.nim`

Provides helper procedures to read inputs. A typical implementation:

```nim
import std/[os, strformat, strutils]

proc readInput*(year: int; day: int; part: int = 1): string =
  ## Reads AoC input from data/{year}/day_{NN}/input_{part}.txt
  ## Tries multiple relative paths so it works from different working dirs.
  let nn = &"{day:02}"

  let candidates = @[
    &"data/{year}/day_{nn}/input_{part}.txt",
    &"../data/{year}/day_{nn}/input_{part}.txt",
    &"../../data/{year}/day_{nn}/input_{part}.txt"
  ]

  for path in candidates:
    if fileExists(path):
      return readFile(path)

  raise newException(IOError,
    "Cannot find input file. Tried:
" & candidates.join("
"))

proc readLines*(year: int; day: int; part: int = 1): seq[string] =
  readInput(year, day, part).splitLines()
```

The `nim/nim.cfg` file contains:

```cfg
path="nim"
```

(or equivalent), so `import aoclib/aoc_input` works without additional `--path` flags.


#### Nim solution skeleton (`nim/aoc_solutions/{year}/day_{NN}.nim`)

A typical day file:

```nim
import std/strutils
import aoclib/aoc_input

const
  Year* = 2017
  Day*  = 1

proc part1*(input: string): int =
  ## TODO: implement part 1
  0

proc part2*(input: string): int =
  ## TODO: implement part 2
  0

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
```

To run a Nim solution from the repo root:

```bash
nim c -r nim/aoc_solutions/2017/day_01.nim
```

Thanks to `nim/nim.cfg`, Nim knows that `nim/` is on the module search path, so `import aoclib/aoc_input` resolves correctly.


---

## Requirements

- **Python**: 3.11+ (tested with 3.12)
- **Rust**: stable toolchain (with `cargo`)
- **Nim**: 2.x (installed e.g. via [choosenim](https://nim-lang.org/install.html))
- Access to an **Advent of Code** account (you need your session cookie to download personal inputs)


### Python dependencies

Listed in `requirements.txt`:

```text
requests
beautifulsoup4
markdownify
python-dotenv
```


---

## Python setup

### 1. Create and activate the virtualenv

From the **repo root**:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 2. Install dependencies

With the venv active:

```bash
pip install -r requirements.txt
```


---

## Advent of Code session (`AOC_SESSION`)

Scripts in `tools/` use your Advent of Code session cookie to download personal inputs.

### 1. Get the cookie value

1. Log in to [https://adventofcode.com](https://adventofcode.com) in your browser.
2. Open developer tools → **Application / Storage / Cookies**.
3. Find the cookie named `session`.
4. Copy **just the value**, a long hex string (without `session=` and without trailing `;`).

### 2. Option A – Global environment variable

Add to your `~/.bashrc` (or a file sourced from it):

```bash
export AOC_SESSION=your_long_cookie_value
```

Then reload:

```bash
source ~/.bashrc
```

Check:

```bash
echo "$AOC_SESSION"
python -c "import os; print(os.getenv('AOC_SESSION'))"
```


---

## `tools/get_day.py`

Downloads **instructions** and **input** for a specific day.

- If you **don’t pass arguments** → uses **today** (`year` and `day` from current date).
- If you pass **only -y or only -d** → error (you must pass both).
- If you pass **both -y and -d** → uses those.

It saves files in:

```text
data/{year}/day_{NN}/
    instructions.md
    input_1.txt
```

Examples:

```bash
# current year/day
./tools/get_day.py

# December 1st, 2024
./tools/get_day.py -y 2024 -d 1
```

The script is idempotent: if the files already exist, it leaves them alone and logs `[SKIP]`.


---

## `tools/new_python.py`

Generates the skeleton for a Python solution:

1. Ensures `instructions.md` and `input_1.txt` exist for `year/day` (reuses `get_day.py`).
2. Creates (if needed) the directory:

   ```text
   python/aoc_solutions/{year}/
   ```

3. Creates the file:

   ```text
   python/aoc_solutions/{year}/day_{NN}.py
   ```

   if it does not exist (if it does → error).

The template uses `GetInput` and exposes `solve_1` / `solve_2`.

Examples:

```bash
# today
./tools/new_python.py

# December 5th, 2024
./tools/new_python.py -y 2024 -d 5
```


---

## `tools/new_rust.py`

Generates the skeleton for a Rust solution:

1. Ensures `instructions.md` and `input_1.txt` exist for `year/day` (reuses `get_day.py`).
2. Assumes `rust/` exists as a workspace and contains crate `aoclib`.
3. Creates (if needed) the crate:

   ```text
   rust/crates/y{year}/
   ```

   with a basic `Cargo.toml` depending on `aoclib`.

4. Adds `crates/y{year}` to the `members` list in `rust/Cargo.toml` (if missing).
5. Creates the bin file:

   ```text
   rust/crates/y{year}/src/bin/day_{NN}.rs
   ```

   if it does not exist (if it does → error).

Examples:

```bash
# today
./tools/new_rust.py

# December 2nd, 2024
./tools/new_rust.py -y 2024 -d 2
```


---

## `tools/new_nim.py`

Generates the skeleton for a Nim solution:

1. Ensures the Nim helper module exists:

   ```text
   nim/aoclib/aoc_input.nim
   ```

   (if missing, it writes a default implementation similar to the one shown above).

2. Creates (if needed) the directory:

   ```text
   nim/aoc_solutions/{year}/
   ```

3. Creates the file:

   ```text
   nim/aoc_solutions/{year}/day_{NN}.nim
   ```

   if it does not exist (if it does → error).

You can then implement `part1` and `part2` in Nim.

Examples:

```bash
# specific day
./tools/new_nim.py 2017 1
./tools/new_nim.py 2017 2
```

Run from repo root:

```bash
nim c -r nim/aoc_solutions/2017/day_01.nim
```


---

## Conventions

- Day names always have 2 digits: `day_01`, `day_02`, …, `day_25`
- Data directories follow: `data/{year}/day_{NN}/`
- All languages read from the same `./data` tree
- Helper modules (`python/get_input.py`, `rust/crates/aoclib`, `nim/aoclib/aoc_input.nim`) abstract away the path logic so per-day solutions can stay focused on algorithms.

The repository is designed to be extended with more languages in the future
(e.g. `./c`, `./haskell`, etc.), always reusing `./data` as the shared input source.
