import std/strutils
import aoclib/aoc_input
import sequtils

const
  Year* = 2025
  Day*  = 3

proc both_parts*(input: string, length: int): int =
  var res: int = 0
  for line in input.strip().splitLines():
    let numbers: seq[int] = line.mapIt(parseInt($it))
    let n = len(numbers)
    var start = 0
    var remaining = length
    var meta = 0

    while remaining > 0:
      let stop = n - remaining
      let window = numbers[start..stop]

      let best = window.max()
      let local_idx = window.maxIndex()
      let idx = start + local_idx
      
      start = idx + 1
      remaining -= 1

      meta = meta * 10 + best

    res += meta

  res


when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", both_parts(input,2)
  echo "Part 2: ", both_parts(input,12)
