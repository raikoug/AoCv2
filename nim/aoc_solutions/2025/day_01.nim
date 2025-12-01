import std/strutils
import aoclib/aoc_input

const
  Year* = 2025
  Day*  = 1

proc part1*(input: string): int =
  var start = 50
  var result = 0
  for line in input.strip().splitLines():
    var s_mult = line[0]
    var s_lenght = line[1 .. ^1]
    var mult = 0
    if s_mult == 'R':
      mult = 1
    elif s_mult == 'L':
      mult = -1
    
    var lenght = parseInt($s_lenght)

    start = (start + (lenght * mult)) mod 100
    if start == 0:
      result += 1

  
  result

proc part2*(input: string): int =
  var start = 50
  var result = 0
  for line in input.strip().splitLines():
    var s_mult = line[0]
    var s_lenght = line[1 .. ^1]
    var mult = 0
    if s_mult == 'R':
      mult = 1
    elif s_mult == 'L':
      mult = -1
    
    var lenght = parseInt($s_lenght)

    for i in 0 .. lenght:
      start = (start + mult) mod 100
      if start == 0:
        result += 1

  
  result

when isMainModule:
  let input = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
