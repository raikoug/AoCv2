# nim/aoclib/aoc_input.nim
import std/[os, strformat, strutils]

proc readInput*(year: int; day: int; part: int = 1): string =
  ## Legge l'input AoC da data/{year}/day_{NN}/input_{part}.txt
  ##
  ## Supporta vari working directory:
  ##   - root repo:        data/...
  ##   - dentro nim/:      ../data/...
  ##   - dentro sorgente:  ../../data/...
  ##
  ## Esempio:
  ##   let s = readInput(2016, 1)  # data/2016/day_01/input_1.txt

  let nn = &"{day:02}"

  let candidates = @[
    &"data/{year}/day_{nn}/input_{part}.txt",
    &"../data/{year}/day_{nn}/input_{part}.txt",
    &"../../data/{year}/day_{nn}/input_{part}.txt"
  ]

  for path in candidates:
    if fileExists(path):
      return readFile(path)

  # Se nessun path funziona, solleva un errore chiaro
  raise newException(IOError,
    "Cannot find input file. Tried:\n" & candidates.join("\n"))

proc readLines*(year: int; day: int; part: int = 1): string =
  ## Ritorna le righe come seq[string]
  readInput(year, day, part)
