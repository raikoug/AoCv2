use std::ops::{Range, RangeInclusive};

use aoclib::read_input;

const YEAR: i32 = 2025;
const DAY: u8 = 5;

fn part1(_input: &str) -> i64 {
    let mut res : i64 = 0;
    let mut ranges: Vec<RangeInclusive<i64>> = Vec::new();
    let mut values: Vec<i64> = Vec::new();

    let mut space: bool = false;

    _input.trim().lines().for_each(|line|{
        if line.is_empty(){
            space = true;
            println!("Change!")
        }
        else{
            if !space {
                ranges.push( line
                    .split_once('-')
                    .map(|(a, b)| {
                        a.parse::<i64>().unwrap()..=(b.parse::<i64>().unwrap())
                    })
                    .unwrap()
                );
            } else {
                values.push(line.trim().parse::<i64>().unwrap());
            }
        }
    });
    
    values.iter().for_each(|n| {
        for r in ranges.clone(){
            if r.contains(n){
                res += 1;
                break
            }
        }
    });

    res
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
