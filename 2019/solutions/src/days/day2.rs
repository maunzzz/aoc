use std::fs;

#[allow(dead_code)]
pub fn solve() {
    match fs::read_to_string("inputs/day2") {
        Ok(input) => {
            task_a(&String::from(input.trim()));
            task_b(&String::from(input.trim()));
        }
        Err(e) => panic!("Unable to read file, error {}", e),
    }
}

fn run_program(ops: &mut Vec<usize>) {
    let mut val1: usize;
    let mut val2: usize;
    let mut dest: usize;
    for i in (0..ops.len()).step_by(4) {
        if ops[i] == 99 {
            break;
        } else if ops[i] == 1 {
            val1 = ops[i + 1];
            val2 = ops[i + 2];
            dest = ops[i + 3];
            ops[dest] = ops[val1] + ops[val2];
        } else if ops[i] == 2 {
            val1 = ops[i + 1];
            val2 = ops[i + 2];
            dest = ops[i + 3];
            ops[dest] = ops[val1] * ops[val2];
        }
    }
}

fn task_a(input_str: &String) {
    let mut ops = Vec::<usize>::new();
    for op in input_str.split(',') {
        ops.push(op.parse().unwrap());
    }

    ops[1] = 12;
    ops[2] = 2;
    run_program(&mut ops);
    println!("a) {}", ops[0])
}

fn task_b(input_str: &String) {
    let mut ops = Vec::<usize>::new();
    for op in input_str.split(',') {
        ops.push(op.parse().unwrap());
    }
    let ops = ops;

    for verb in 0..100 {
        for noun in 0..100 {
            let mut this_ops = ops.clone();
            this_ops[1] = noun;
            this_ops[2] = verb;
            run_program(&mut this_ops);
            if this_ops[0] == 19690720 {
                println!("b) {}", 100 * noun + verb);
                return;
            }
        }
    }
}
