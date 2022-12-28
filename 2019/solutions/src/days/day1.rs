use crate::utils;

#[allow(dead_code)]
pub fn solve() {
    let inp = utils::read_as_vector_of_numbers::<u32>("inputs/day1");

    let mut res = 0u32;
    for val in inp.iter() {
        res += (val / 3) - 2;
    }

    println!("a) {}", res);

    let mut res = 0u32;
    for val in inp {
        let mut fuel = val;
        while fuel >= 9 {
            fuel = (fuel / 3) - 2;
            res += fuel;
        }
    }
    println!("b) {}", res);
}
