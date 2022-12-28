use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

struct Policy {
    low: u32,
    high: u32,
    letter: char,
}

fn main() {
    let mut passwords = Vec::<String>::new();
    let mut policies = Vec::<Policy>::new();

    if let Ok(lines) = read_lines("inputs/day2") {
        for line in lines {
            if let Ok(ip) = line {    
                let mut ip = String::from(ip.trim());
                ip = ip.replace("-", " ").replace(":", " ");
                let v: Vec<&str> = ip.split(" ").collect();

                let low: u32 = v[0].parse().expect("Failed parsing");
                let high: u32 = v[1].parse().expect("Failed parsing");
                let letter: char = v[2].chars().next().unwrap();
                
                policies.push(Policy { low, high, letter });
                passwords.push( String::from(v[4]) );
            }
        }
    }
    let passwords = passwords;
    let policies = policies; 

    let mut n_valid_passwords: u32 = 0;
    let mut n_valid_passwords_b: u32 = 0;
    for pp in passwords.iter().zip(policies.iter()){
        let (pw, pol) = pp;
        n_valid_passwords += eval_password(pw, pol);
        n_valid_passwords_b += eval_password_b(pw, pol);
    }

    println!("a) {}", n_valid_passwords);
    println!("b) {}", n_valid_passwords_b);
}

fn eval_password(pw: &String, pol: &Policy) -> u32{
    let mut count: u32 = 0;
    for c in pw.chars(){
        if c == pol.letter {
            count += 1;
        }
    }
    if (count >= pol.low) & (count <= pol.high){
        return 1
    }
    0
}

fn eval_password_b(pw: &String, pol: &Policy) -> u32{
    let chars: Vec<char> = pw.chars().collect();
    if (pol.letter == chars[(pol.low - 1) as usize]) ^ (pol.letter == chars[(pol.high - 1) as usize]){
        return 1
    }
    0
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
