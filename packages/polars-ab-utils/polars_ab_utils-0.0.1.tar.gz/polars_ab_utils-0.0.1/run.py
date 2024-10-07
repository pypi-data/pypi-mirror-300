import polars as pl
from polars_ab_utils import get_bucket

df = pl.DataFrame(
    {
        "user_id": [
            "576802932",
            "412120092",
            "579966747",
            "494077766",
            "560109803",
        ],
        "age": [
            31,
            16,
            24,
            44,
            21,
        ],
    }
)

print(
    df.select(
        get_bucket(
            pl.col("user_id"),
            hash_algorithm="md5",
            num_buckets=20,
        )
    )
)
