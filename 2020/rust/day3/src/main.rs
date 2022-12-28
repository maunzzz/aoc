use aoc_utils::read::read_lines;
use ndarray::prelude::{Array, Ix2};

fn main() {
    let mut input = Vec::<String>::new();

    match read_lines("inputs/day3") {
        Ok(lines) => {
            for line in lines {
                if let Ok(ip) = line {
                    input.push(String::from(ip.trim()));
                }
            }
        }
        Err(e) => panic!("Unable to read file, error {}", e),
    }

    let mut data = Array::<u8, Ix2>::zeros((input.len(), input[0].len()));
    for row in 0..input.len() {
        for col in 0..input[row].len() {
            if input[row].chars().nth(col).unwrap() == '#' {
                data[[row, col]] = 1;
            }
        }
    }

    let dir = (1, 3);
    println!("a) {}", evaluate_direction(dir, &data));

    let slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)];
    let mut prod = 1u128;
    for dir in slopes.iter() {
        prod *= evaluate_direction(*dir, &data)
    }
    println!("b) {}", prod);
}

fn evaluate_direction(dir: (usize, usize), treemap: &Array<u8, Ix2>) -> u128 {
    let mut rowpos = 0usize;
    let mut colpos = 0usize;
    let mut n_collisions = 0u128;
    while rowpos < treemap.nrows() {
        n_collisions += treemap[[rowpos, colpos]] as u128;
        rowpos += dir.0;
        colpos = (colpos + dir.1) % treemap.ncols();
    }
    n_collisions
}
