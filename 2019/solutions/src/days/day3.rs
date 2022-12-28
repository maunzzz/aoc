use crate::utils;
use std::collections::HashMap;

#[allow(dead_code)]
pub fn solve() {
    let max_val = 100_000;

    let input = utils::read_as_vector_of_strings("inputs/day3");
    let mut grid = HashMap::new();

    let mut posx = 0;
    let mut posy = 0;
    let mut steps_from_start = 0;
    grid.insert(max_val * posx + posy, 1);

    // wire 1
    for move_str in input[0].split(',') {
        let (diffx, diffy, steps) = parse_move(move_str);
        for _ in 0..steps {
            posx += diffx;
            posy += diffy;
            steps_from_start += 1;

            if !grid.contains_key(&(max_val * posx + posy)) {
                grid.insert(max_val * posx + posy, steps_from_start);
            }
        }
    }

    posx = 0;
    posy = 0;
    steps_from_start = 0;
    let mut distance_to_closest = 2 * max_val;
    let mut distance_to_closest_b = 2 * max_val;
    // wire 2
    for move_str in input[1].split(',') {
        let (diffx, diffy, steps) = parse_move(move_str);
        for _ in 0..steps {
            posx += diffx;
            posy += diffy;
            steps_from_start += 1;

            // intersection
            if grid.contains_key(&(max_val * posx + posy)) {
                let dist = posx.abs() + posy.abs();
                if dist < distance_to_closest {
                    distance_to_closest = dist;
                }

                let steps_from_start1 = grid.get(&(max_val * posx + posy)).unwrap();
                if *steps_from_start1 + steps_from_start < distance_to_closest_b {
                    distance_to_closest_b = *steps_from_start1 + steps_from_start;
                }
            }
        }
    }
    println!("a) {}", distance_to_closest);
    println!("a) {}", distance_to_closest_b);
}

fn parse_move(move_str: &str) -> (i32, i32, u32) {
    let mut move_str = String::from(move_str);
    let dir = move_str.remove(0);
    let steps: u32 = move_str.parse().expect("Parsing Error");
    let mut diffx = 0;
    let mut diffy = 0;
    if dir == 'R' {
        diffx = 1;
    } else if dir == 'L' {
        diffx = -1;
    } else if dir == 'U' {
        diffy = -1;
    } else if dir == 'D' {
        diffy = 1;
    }
    (diffx, diffy, steps)
}
