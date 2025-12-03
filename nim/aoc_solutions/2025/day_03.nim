import std/strutils
import aoclib/aoc_input

const
  Year* = 2025
  Day*  = 3

proc part1*(input: string): string =

  discard
  result = ""

proc part2*(input: string): string =

  discard
  result = ""

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
