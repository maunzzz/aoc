use aoc_utils::read::read_lines;

fn main() {
    let mut numbers = Vec::<i32>::new();

    if let Ok(lines) = read_lines("inputs/day1") {
        for line in lines {
            if let Ok(ip) = line {
                numbers.push(ip.trim().parse().expect("Failed parsing"));
            }
        }
    }

    let numbers = numbers; // Freeze input, making it immutable

    match find_pair(&numbers) {
        Some(res) => println!("a) {}", res),
        None => println!("a) No sum found"),
    }

    match find_triplet(&numbers) {
        Some(res) => println!("b) {}", res),
        None => println!("b) No sum found"),
    }
}

fn find_pair(numbers: &Vec<i32>) -> Option<i32> {
    for num1 in numbers.iter() {
        for num2 in numbers.iter() {
            if *num1 + *num2 == 2020 {
                return Some(*num1 * *num2);
            }
        }
    }
    None
}

fn find_triplet(numbers: &Vec<i32>) -> Option<i32> {
    for num1 in numbers.iter() {
        for num2 in numbers.iter() {
            for num3 in numbers.iter() {
                if *num1 + *num2 + *num3 == 2020 {
                    return Some(*num1 * *num2 * *num3);
                }
            }
        }
    }
    None
}
