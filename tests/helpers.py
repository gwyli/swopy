from collections.abc import Callable
from fractions import Fraction
from math import ceil, floor
from types import FunctionType, UnionType
from typing import Any

from hypothesis import strategies as st

from swopy import System, get_all_systems

from .system_strategies import SYSTEM_STRATEGIES

SYSTEMS: list[type[System[Any, Any]]] = list(get_all_systems().values())


TYPE_STRATEGY_MAP: dict[UnionType | type, FunctionType] = {
    str: st.integers,
    int: st.integers,
    float: st.floats,
    Fraction: st.fractions,
}


def min_max(
    operator: Callable[..., Any],
    min_val: int | Fraction | float,
    max_val: int | Fraction | float,
) -> int:
    """ """

    return operator(ceil(min_val), floor(max_val))


def construct_union_strategy(
    system: type[System[Any, Any]], is_successful: bool
) -> st.SearchStrategy:
    """Compose existing single-type strategies for a union-accepting class."""

    component_strategies = [
        x.strategy for x in SYSTEM_STRATEGIES[system] if x.is_succesful == is_successful
    ]
    return st.one_of(*component_strategies)
