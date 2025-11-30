import std/[strutils, tables, math]
import aoclib/aoc_input

const
  Year* = 2017
  Day*  = 3

type
  Coord = tuple[x, y: int]

const
  turns: array[4, Coord] = [
    (x:  1, y:  0),  # right
    (x:  0, y:  1),  # up
    (x: -1, y:  0),  # left
    (x:  0, y: -1)   # down
  ]

  neighborOffsets: array[8, Coord] = [
    (x: -1, y:  1), (x:  0, y:  1), (x:  1, y:  1),
    (x: -1, y:  0),                  (x:  1, y:  0),
    (x: -1, y: -1), (x:  0, y: -1), (x:  1, y: -1)
  ]

proc getCoordinateOf(target: int): Coord =
  ## Ritorna le coordinate cartesiane (x,y) della cella "target" nella spirale.
  if target == 1:
    return (x: 0, y: 0)

  var
    turnIndex = 0
    distance  = 1
    value     = 1
    steps     = 0
    actual    = (x: 0, y: 0)

  while true:
    let turn = turns[turnIndex]
    let nextPos = (
      x: actual.x + turn.x * distance,
      y: actual.y + turn.y * distance
    )
    actual = nextPos

    value += distance
    inc steps

    # prossimo lato della spirale
    turnIndex = (turnIndex + 1) mod 4
    if steps mod 2 == 0:
      inc distance

    if value >= target:
      let delta = value - target
      result = (
        x: actual.x - turn.x * delta,
        y: actual.y - turn.y * delta
      )
      break

proc tryGetAdj(grid: Table[Coord, int], x, y: int): int =
  var sum = 0
  for off in neighborOffsets:
    let pos = (x: x + off.x, y: y + off.y)
    if grid.hasKey(pos):
      sum += grid[pos]
  result = sum

proc getFirstLarger(target: int): int =
  var
    turnIndex = 0
    distance  = 1
    value     = 1
    steps     = 0
    actual    = (x: 0, y: 0)
    grid      = initTable[Coord, int]()

  grid[actual] = 1

  while true:
    let turn = turns[turnIndex]
    for _ in 0 ..< distance:
      let nextPos = (
        x: actual.x + turn.x,
        y: actual.y + turn.y
      )
      actual = nextPos

      value = tryGetAdj(grid, actual.x, actual.y)
      if value > target:
        result = value
        return

      grid[actual] = value

    inc steps
    turnIndex = (turnIndex + 1) mod 4
    if steps mod 2 == 0:
      inc distance

proc part1*(input: string): string =
  let target = input.strip.parseInt
  let c = getCoordinateOf(target)
  let dist = abs(c.x) + abs(c.y)
  result = $dist

proc part2*(input: string): string =
  let target = input.strip.parseInt
  let v = getFirstLarger(target)
  result = $v

when isMainModule:
  let input: string = readInput(Year, Day)
  echo "Part 1: ", part1(input)
  echo "Part 2: ", part2(input)
