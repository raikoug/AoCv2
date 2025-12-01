import std/strutils
import aoclib/aoc_input
import sequtils

const
  Year* = 2017
  Day*  = 6

proc part1*(input: string): int =

  var registers: seq[int] = input.strip().splitWhitespace().map(parseInt)
  var steps = 0
  var history: seq[seq[int]] = @[]

  history.add(registers)

  while true:
    var index = maxIndex(registers)
    var val = registers[index]
    registers[index] = 0
    for _ in 1..val:
      index = (index + 1) mod len(registers)
      registers[index] += 1
    
    steps += 1
    if history.contains(registers):
      return steps

    history.add(registers)
    

proc part2*(input: string): int =

  var registers: seq[int] = input.strip().splitWhitespace().map(parseInt)
  var steps = 0
  var history: seq[seq[int]] = @[]

  history.add(registers)

  while true:
    var index = maxIndex(registers)
    var val = registers[index]
    registers[index] = 0
    for _ in 1..val:
      index = (index + 1) mod len(registers)
      registers[index] += 1
    
    steps += 1
    if history.contains(registers):
      break

    history.add(registers)
  
  let first_index = findIt(history, it == registers)
  steps - first_index

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
