from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from polars_ab_utils._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_ab_utils.typing import IntoExprColumn

LIB = Path(__file__).parent


def get_bucket(
    expr: IntoExprColumn,
    *,
    hash_algorithm: str = "sha256",
    num_buckets: int = 10,
    salt: str = "",
) -> pl.Expr:
    SUPPORTED_HASH_AGLORITHMS = (
        "sha256",
        "md5",
    )

    if hash_algorithm not in SUPPORTED_HASH_AGLORITHMS:
        raise RuntimeError(
            "Unknown hash algorithm. Supported hash algoritms `md5` or `sha256`"
        )
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="get_bucket",
        is_elementwise=True,
        kwargs={
            "hash_algorithm": hash_algorithm,
            "num_buckets": num_buckets,
            "salt": salt,
        },
    )
