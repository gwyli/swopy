from fractions import Fraction
from types import FunctionType, NoneType, UnionType, get_original_bases
from typing import Any, get_args

from hypothesis import strategies

from numberology import RealNumber, System, get_all_systems

SYSTEMS: list[type[System[Any]]] = list(get_all_systems().values())
SYSTEMS_WITHOUT_ARABIC: list[type[System[Any]]] = [
    s for s in get_all_systems().values() if s.__name__ != "Arabic"
]

TYPE_STRATEGY_MAP: dict[UnionType | type, FunctionType] = {
    str: strategies.integers,
    int: strategies.integers,
    RealNumber: strategies.floats,
    float: strategies.floats,
    Fraction: strategies.fractions,
}


def base_types(obj: type) -> tuple[type]:
    """Returns the base type of the numeral system. When multiple types are
    supported, unfurl the UnionType and return all base types.

    Returns:
        The base type(s) used for numeral representation in this system.
    """
    type_ = obj
    original_base: type = get_original_bases(type_)[0]
    types: tuple[type | NoneType | UnionType] = get_args(original_base)

    # Occurs if the class is subclassed without specifying a type parameter.
    # Walk back to the original base to get the correct type parameter.
    if types == ():
        return base_types(obj=original_base)

    if isinstance(types[0], UnionType):
        return get_args(types[0])

    if isinstance(types[0], NoneType):
        raise ValueError("Numeral system base type cannot be NoneType.")

    return (types[0],)
