from fractions import Fraction
from types import FunctionType, UnionType
from typing import Any

from hypothesis import strategies

from numberology import System, get_all_systems

SYSTEMS: list[type[System[Any, Any]]] = list(get_all_systems().values())
SYSTEMS_WITHOUT_ARABIC: list[type[System[Any, Any]]] = [
    s for s in get_all_systems().values() if s.__name__ != "Arabic"
]

TYPE_STRATEGY_MAP: dict[UnionType | type, FunctionType] = {
    str: strategies.integers,
    int: strategies.integers,
    float: strategies.floats,
    Fraction: strategies.fractions,
}


def everything_except(
    excluded_types: tuple[type | UnionType, ...],
) -> strategies.SearchStrategy[Any]:
    """Generate arbitrary values excluding instances of specified types.

    Args:
        excluded_types: A type or tuple of types to exclude from generation.

    Returns:
        A strategy that generates values not matching the excluded type(s).
    """
    return (
        strategies.from_type(object)
        .map(type)
        .filter(lambda x: not isinstance(x, excluded_types))
    )
