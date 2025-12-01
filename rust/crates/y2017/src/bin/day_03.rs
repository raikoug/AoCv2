use std::path::absolute;

use aoclib::read_input;

const YEAR: i32 = 2017;
const DAY: u8 = 3;

fn part1(input: &str) -> i64 {
    let target: i64 = input.trim().parse().expect("Not an int!");
    let mut res: i64 = 0;
    let directions: [(i64, i64); 4] = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ];
    let mut turn_index: usize = 0;
    let mut distance  : i64   = 1;
    let mut value     : i64   = 1;
    let mut actualx   : i64   = 0;
    let mut actualy   : i64   = 0;
    let mut steps     : i64   = 0;


    let mut result_x: i64 = 0;
    let mut result_y: i64 = 0;

    while true {
        let direction = directions[turn_index];
        let nextx = actualx + direction.0 * distance;
        let nexty = actualy + direction.1 * distance;

        actualx = nextx;
        actualy = nexty;


        value += distance;
        steps += 1;

        turn_index += 1;
        turn_index = turn_index % 4;

        if steps % 2 == 0 {
            distance += 1
        }

        if value >= target{
            let delta: i64 = value - target;
            result_x = actualx - direction.0 * delta;
            result_y = actualy - direction.1 * delta;

            break
        }
    }


    result_x.abs() + result_y.abs()
}

fn part2(_input: &str) -> i64 {
    // TODO: implementa la logica della parte 2
    0
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
