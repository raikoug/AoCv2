import std/strutils
import aoclib/aoc_input
from strformat import fmt

const
  Year* = 2017
  Day*  = 1

proc part1*(input: string): int =
  let stringa: string =  "$1$2" % [input.strip(), $input[0]]
  var result = 0
  for i, ch in stringa:
    if i + 1 < len(stringa):
      let val = parseInt($ch)
      let next_val = parseInt($stringa[i+1])
      if val == next_val:
        result += val

  result

proc part2*(input: string): int =
  var stringa = input.strip()
  var result = 0
  let module = len(stringa)
  let distance : int = (len(stringa) / 2).toInt()
  for i, ch in stringa:
    let val = parseInt($ch)
    var index_to_check: int = (i + distance) mod module
    var var_to_check = parseInt($stringa[index_to_check])
    if val == var_to_check:
      result += val


  result

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
