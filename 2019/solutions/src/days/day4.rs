#[allow(dead_code)]
pub fn solve() {
    let lower = 197487;
    let upper = 673251;

    let mut num_valid_pws = 0;
    let mut num_valid_pws_b = 0;
    for pw in lower..(upper + 1) {
        if check_validity(pw, true) {
            num_valid_pws += 1;
        }
        if check_validity(pw, false) {
            num_valid_pws_b += 1;
        }
    }
    println!("a) {}", num_valid_pws);
    println!("b) {}", num_valid_pws_b);
}

fn check_validity(pw: i32, allow_more_than_two: bool) -> bool {
    let mut any_equal = false;
    for i in 0..5 {
        let this_num = (pw / (10i32.pow(i))) % 10;
        let prev_num = (pw / (10i32.pow(i + 1))) % 10;
        if this_num < prev_num {
            return false;
        }
        if this_num == prev_num {
            if allow_more_than_two {
                any_equal = true;
            } else {
                if i != 5 {
                    let prev_prev_num = (pw / (10i32.pow(i + 2))) % 10;
                    if prev_prev_num == this_num {
                        continue;
                    }
                }
                if i != 0 {
                    let next_num = (pw / (10i32.pow(i - 1))) % 10;
                    if next_num == this_num {
                        continue;
                    }
                }
                any_equal = true;
            }
        }
    }
    any_equal
}
