use aoclib::read_input;

const YEAR: i32 = 2025;
const DAY: u8 = 1;

fn part1(input: &str) -> i64 {
    let mut result : i64 = 0;
    let mut start : i64 = 50;
    
    input
    .lines()
    .filter(|l| !l.is_empty())
    .for_each(|line|{
        let (dir, num_str) = line.split_at(1);

        let mult: i64 = match dir {
                "R" => 1,
                "L" => -1,
                _ => 0,
            };

        let number: i64 = num_str
                .trim()
                .parse()
                .expect("numero non valido nell'input");

        start = (start + (number * mult)).rem_euclid(100);

        if start == 0{
            result += 1;
        }
    });

    result
}

fn part2(input: &str) -> i64 {
    let mut result : i64 = 0;
    let mut start : i64 = 50;
    
    input
    .lines()
    .filter(|l| !l.is_empty())
    .for_each(|line|{
        let (dir, num_str) = line.split_at(1);

        let step: i64 = match dir {
                "R" => 1,
                "L" => -1,
                _ => 0,
            };

        let number: i64 = num_str
                .trim()
                .parse()
                .expect("numero non valido nell'input");
        
        for _i in 0..number {
            start = (start + (step)).rem_euclid(100);

            if start == 0 {
                result += 1;
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
