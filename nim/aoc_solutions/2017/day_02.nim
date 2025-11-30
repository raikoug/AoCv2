import std/strutils
import aoclib/aoc_input
import std/sequtils

const
  Year* = 2017
  Day*  = 2

proc part1*(input: string): int =
  let righe = input.strip().splitLines()
  var result: int = 0

  for riga in righe:
    let pieces = riga.splitWhitespace()
    var lower : int = 9999999999
    var maximum : int = 0
    for piece in pieces:
      if parseInt(piece) < lower: lower = parseInt(piece)
      if parseInt(piece) > maximum: maximum = parseInt(piece)

    var delta = maximum - lower

    result += delta

  result

proc part2*(input: string): int =
  let righe = input.strip().splitLines()
  var result: int = 0

  for riga in righe:
    let nums = riga.splitWhitespace().map(parseInt)

    block row:
      for i in 0 ..< nums.len:
        for j in 0 ..< nums.len:
          if i == j:
            continue
          let a = nums[i]
          let b = nums[j]
          if a mod b == 0:
            result += a div b
            break row


  result

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
