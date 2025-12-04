use aoclib::read_input;

const YEAR: i32 = 2025;
const DAY: u8 = 3;

fn bank_joltage(line: &str, k: usize) -> i64 {
    let digits: Vec<u8> = line
        .trim()
        .bytes()
        .map(|b| b - b'0')
        .collect();

    let n = digits.len();
    let mut start = 0;
    let mut remaining = k;
    let mut meta: i64 = 0;

    while remaining > 0 {
        let stop = n - remaining;

        let (best_rel_idx, best_digit) = digits[start..=stop]
            .iter()
            .enumerate()
            .max_by_key(|&(_i, d)| d)
            .map(|(i, d)| (i, *d))
            .expect("slice non vuota");

        let idx = start + best_rel_idx;

        meta = meta * 10 + best_digit as i64;

        start = idx + 1;
        remaining -= 1;
    }

    meta
}

fn both(input: &str, l: usize) -> i64 {
    input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|line| bank_joltage(line, l))
        .sum()
    
}



fn main() {
    let input = read_input(YEAR, DAY, 1).expect("cannot read input");
    println!("Part 1: {}", both(&input, 2));
    println!("Part 2: {}", both(&input, 12));
}
