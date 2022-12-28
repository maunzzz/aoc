#![allow(dead_code)]

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::str::FromStr;

// reads an input file line by line, returns iterator
pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

// read file line by line and returns vector of Strings
pub fn read_as_vector_of_strings(filename: &str) -> Vec<String> {
    let mut input = Vec::<String>::new();
    match read_lines(filename) {
        Ok(lines) => {
            for line in lines {
                if let Ok(ip) = line {
                    input.push(String::from(ip.trim()));
                }
            }
        }
        Err(e) => panic!("Unable to read file, error {}", e),
    }
    input
}

// read file line by line and store as datatype F
// e.g. utils::read_as_vector_of_numbers::<u32>("inputs/day1");
pub fn read_as_vector_of_numbers<F: FromStr>(filename: &str) -> Vec<F> {
    let mut numbers = Vec::<F>::new();

    match read_lines(filename) {
        Ok(lines) => {
            for line in lines {
                if let Ok(ip) = line {
                    match ip.trim().parse::<F>() {
                        Ok(number) => numbers.push(number),
                        Err(_) => {
                            if ip.len() > 0 {
                                println!("Unable to parse {}", ip)
                            }
                        }
                    }
                }
            }
        }
        Err(e) => panic!("Unable to read file, error {}", e),
    }
    numbers
}
