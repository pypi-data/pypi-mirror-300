#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

use crate::hash_functions::{md5_hash_sum, sha256_hash_num};
use std::str::FromStr;

#[derive(Debug, PartialEq)]
enum HashAlgorithmType {
    SHA256,
    MD5,
}

impl FromStr for HashAlgorithmType {
    type Err = ();

    fn from_str(input: &str) -> Result<HashAlgorithmType, Self::Err> {
        match input {
            "sha256" => Ok(HashAlgorithmType::SHA256),
            "md5" => Ok(HashAlgorithmType::MD5),
            _ => Err(()),
        }
    }
}

#[derive(Deserialize)]
struct GetBucketKwargs {
    hash_algorithm: String,
    num_buckets: u8,
    salt: String,
}

#[polars_expr(output_type=UInt8)]
fn get_bucket(inputs: &[Series], kwargs: GetBucketKwargs) -> PolarsResult<Series> {
    let ca: &StringChunked = inputs[0].str()?;
    let out: Vec<Option<u8>> = ca
        .into_iter()
        .map(|opt_value| match opt_value {
            Some(value) => {
                let hash_algorithm_type =
                    HashAlgorithmType::from_str(&kwargs.hash_algorithm).unwrap();
                match hash_algorithm_type {
                    HashAlgorithmType::SHA256 => {
                        Some(sha256_hash_num(value, kwargs.num_buckets, &kwargs.salt))
                    },
                    HashAlgorithmType::MD5 => {
                        Some(md5_hash_sum(value, kwargs.num_buckets, &kwargs.salt))
                    },
                }
            },
            _ => None,
        })
        .collect();
    Ok(Series::new("num_bucket".into(), out))
}
