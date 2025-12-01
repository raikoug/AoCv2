use aoclib::read_input;

const YEAR: i32 = 2017;
const DAY: u8 = 2;

fn part1(input: &str) -> i64 {
    let mut result: i64 = 0;
    input
        .trim()
        .lines()
        .filter(|l| !l.trim().is_empty())
        .for_each(|line| {
            let nums: Vec<i64> = line
             .split_whitespace()
             .map(|c: &str| c.parse::<i64>()
             .expect("Not an int"))
             .collect();

            let min = nums.iter().min().unwrap();
            let max = nums.iter().max().unwrap();
            result += max - min
        });
    result
}

fn part2(input: &str) -> i64 {
    let mut result: i64 = 0;
    input
        .trim()
        .lines()
        .filter(|l| !l.trim().is_empty())
        .for_each(|line| {
            let nums: Vec<i64> = line
             .split_whitespace()
             .map(|c: &str| c.parse::<i64>()
             .expect("Not an int"))
             .collect();

            for (i, &a) in nums.iter().enumerate() {
                for &b in &nums[i + 1..] {
                    let (max, min) = if a > b { (a, b) } else { (b, a) };
                    if max % min == 0 {
                        result += max / min
                    }
                }
            }
        });
    result
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
