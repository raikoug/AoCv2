use aoclib::read_input;

const YEAR: i32 = 2017;
const DAY: u8 = 1;

fn part1(input: &str) -> u32 {
    let digits: Vec<u32> = input
        .trim()
        .chars()
        .map(|c| c.to_digit(10).expect("not a digit"))
        .collect();

    let len = digits.len();

    (0..len)
        .filter(|&i| digits[i] == digits[(i + 1) % len])
        .map(|i| digits[i])
        .sum()
}

fn part2(input: &str) -> u32 {
    let digits: Vec<u32> = input
        .trim()
        .chars()
        .map(|c| c.to_digit(10).expect("not a digit"))
        .collect();

    let len = digits.len();
    let half_len: usize = len / 2;
    
    (0..len)
        .filter(|&i| digits[i] == digits[(i + half_len) % len])
        .map(|i| digits[i])
        .sum()
}

fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
