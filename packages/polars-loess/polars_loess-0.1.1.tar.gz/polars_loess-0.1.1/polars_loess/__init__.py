from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

from polars_loess._internal import __version__ as __version__
from polars_loess.utils import parse_into_expr, register_plugin, parse_version

if TYPE_CHECKING:
    from polars.type_aliases import IntoExpr

if parse_version(pl.__version__) < parse_version("0.20.16"):
    from polars.utils.udfs import _get_shared_lib_location

    lib: str | Path = _get_shared_lib_location(__file__)
else:
    lib = Path(__file__).parent


def loess(x: IntoExpr, y: IntoExpr, newx: IntoExpr, *, frac: float = None, points: int = None, degree: int = None) -> pl.Expr:
    return register_plugin(
        args=[x, y, newx],
        symbol="loess",
        is_elementwise=True,
        lib=lib,
        kwargs={"frac": frac, "points": points, "degree": degree},
    )

