import std/strutils
import aoclib/aoc_input
import sequtils

const
  Year* = 2017
  Day*  = 5

proc part1*(input: string): int =
  var instructions : seq[int] = input.strip().splitLines().map(parseInt)

  var index = 0
  var steps = 0
  while index < len(instructions):
    var next_index = index + instructions[index]
    instructions[index] += 1
    index = next_index
    steps += 1


  result = steps

proc part2*(input: string): int =
  var instructions : seq[int] = input.strip().splitLines().map(parseInt)

  var index = 0
  var steps = 0
  while index < len(instructions):
    var next_index = index + instructions[index]
    if instructions[index] >= 3:
      instructions[index] -= 1
    else:
      instructions[index] += 1
    index = next_index
    steps += 1


  result = steps

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
