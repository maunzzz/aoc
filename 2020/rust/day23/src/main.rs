use std::collections::VecDeque;

fn play_game(cups: &mut VecDeque<u32>, n_rounds: u64){
    
    let max_val = cups.len();
    let mut current_num = *cups.get_mut(0).unwrap();
    let mut picked_cups: VecDeque<u32> = VecDeque::with_capacity(3);

    for i in 0..n_rounds {

        while *cups.get(max_val-1).unwrap() != current_num {
            cups.rotate_left(1);
        }

        for _i in 0..3 {
            picked_cups.push_back(cups.pop_front().unwrap());
        }

        let mut destination: u32;
        if current_num == 1 {
            destination = max_val as u32;
        }else{
            destination = current_num - 1;
        }
        
        while picked_cups.contains(&destination) {
            if destination == 1 {
                destination = max_val as u32;
            }else{
                destination -= 1;
            }
        }

        while *cups.get(max_val-4).unwrap() != destination {
            cups.rotate_right(1);
        }

        for _i in 0..3 {
            cups.push_back(picked_cups.pop_front().unwrap());
        }

        while *cups.get(max_val-1).unwrap() != current_num {
            cups.rotate_left(1);
        }
        current_num = *cups.get_mut(0).unwrap();

        if i % 100000 == 0{
            println!("iteration {}", i);
        }
    }
}

fn main() {
    
    let mut cups: VecDeque<u32> = vec![9,1,6,4,3,8,2,7,5].into_iter().collect();
    let mut cups_b: VecDeque<u32> = cups.clone();

    play_game(&mut cups, 100);
    
    let max_val = cups.len();
    while *cups.get(max_val-1).unwrap() != 1 {
        cups.rotate_left(1);
    }
    print!("a) ");
    for _i in 0..8 {
        print!("{}", cups.pop_front().unwrap());
    }
    println!();

    for i in 10..=1000_000 {
        cups_b.push_back(i)
    }

    play_game(&mut cups_b, 10_000_000);
    while *cups_b.get(max_val-1).unwrap() != 1 {
        cups_b.rotate_left(1);
    }

    let p1 = cups_b.pop_front().unwrap() as u128;
    let p2 = cups_b.pop_front().unwrap() as u128;
    println!("b) {}", p1 * p2);
}
