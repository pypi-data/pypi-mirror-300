use num::{BigInt, Num};
use sha2::{Digest, Sha256};
use std::fmt::Write;

pub fn sha256_hash_num(data: &str, num_buckets: u8, salt: &str) -> u8 {
    let mut data = String::from(data);
    if !salt.is_empty() {
        data.push_str(salt);
    }
    let hash = Sha256::digest(data);
    let mut output = String::new();
    write!(output, "{:x}", hash).unwrap();
    let hex_as_number = BigInt::from_str_radix(&output, 16).unwrap();
    let hex_as_number = hex_as_number % num_buckets;
    hex_as_number.to_str_radix(10).parse::<u8>().unwrap()
}

pub fn md5_hash_sum(data: &str, num_buckets: u8, salt: &str) -> u8 {
    let mut data = String::from(data);
    if !salt.is_empty() {
        data.push_str(salt);
    }
    let hash = md5::compute(&data);
    let mut output = String::new();
    write!(output, "{:x}", hash).unwrap();
    let hex_as_number = BigInt::from_str_radix(&output, 16).unwrap();
    let hex_as_number = hex_as_number % num_buckets;
    hex_as_number.to_str_radix(10).parse::<u8>().unwrap()
}
