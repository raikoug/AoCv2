use aoclib::read_input;

const YEAR: i32 = 2025;
const DAY: u8 = 2;

fn is_invalid_id(num: i64) -> bool {
    let s = num.to_string();
    if s.len() % 2 != 0 {
        return false;
    }
    let half = s.len() / 2;
    let (a, b) = s.split_at(half);
    a == b
}

fn is_invalid_id_v2(num: i64) -> bool {
    let s = num.to_string();
    let l: usize = s.len() as usize;
    let h = l / 2; 

    for i in 1..=h{
        if (l % i) != 0{
            continue;
        }
        let sub = s.split_at(i).0;

        if sub.repeat(l / i) == s{
            return true
        }
    }

    false
    
}

fn part1(input: &str) -> i64 {
    input
        .trim()
        .split(',')
        .flat_map(|range| {
            let (low_s, up_s) = range.split_once('-').unwrap();
            let lower = low_s.parse::<i64>().unwrap();
            let upper = up_s.parse::<i64>().unwrap();
            lower..=upper
        })
        .filter(|&num| is_invalid_id(num))
        .sum()
}

fn part2(input: &str) -> i64 {
    input
        .trim()
        .split(',')
        .flat_map(|range| {
            let (low_s, up_s) = range.split_once('-').unwrap();
            let lower = low_s.parse::<i64>().unwrap();
            let upper = up_s.parse::<i64>().unwrap();
            lower..=upper
        })
        .filter(|&num| is_invalid_id_v2(num))
        .sum()
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
