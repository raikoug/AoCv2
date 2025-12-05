use std::ops::RangeInclusive;

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
    let mut ranges: Vec<(i64, i64)> = Vec::new();

    for line in _input.trim().lines(){
        if line.is_empty(){
            break;
        }
        else{
            let (a, b) = line.split_once('-').unwrap();
            let start = a.parse::<i64>().unwrap();
            let end   = b.parse::<i64>().unwrap();
            ranges.push((start, end));

        }
    }
    ranges.sort_unstable_by_key(|&(start, _)| start);

    let (mut cur_start, mut cur_end) = ranges[0];
    let mut total: i64 = 0;

    for (s, e) in ranges.into_iter().skip(1) {
        if s > cur_end + 1 {
            total += cur_end - cur_start + 1;
            cur_start = s;
            cur_end = e;
        } else {
            if e > cur_end {
                cur_end = e;
            }
        }
    }
    total += cur_end - cur_start + 1;

    total

}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
