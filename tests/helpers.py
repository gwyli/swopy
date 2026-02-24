from collections.abc import Callable
from fractions import Fraction
from math import ceil, floor
from types import FunctionType, UnionType
from typing import Any

from hypothesis import strategies as st

from swopy import System, get_all_systems
from swopy.systems import arabic, egyptian, roman

from .strategies import base12_fractions

SYSTEMS: list[type[System[Any, Any]]] = list(get_all_systems().values())
SYSTEMS_WITHOUT_ARABIC: list[type[System[Any, Any]]] = [
    s for s in get_all_systems().values() if s.__name__ != "Arabic"
]

POSITIVE_STRATEGY_CACHE: dict[type[System[Any, Any]], st.SearchStrategy] = {
    arabic.Arabic: st.one_of(
        st.integers(
            min_value=int(arabic.Arabic.minimum), max_value=int(arabic.Arabic.maximum)
        ),
        st.floats(min_value=arabic.Arabic.minimum, max_value=arabic.Arabic.maximum),
        st.fractions(),
    ),
    egyptian.Egyptian: st.integers(
        min_value=int(egyptian.Egyptian.minimum),
        max_value=int(egyptian.Egyptian.maximum),
    ),
    roman.Early: st.integers(
        min_value=int(roman.Early.minimum), max_value=int(roman.Early.maximum)
    ),
    roman.Standard: st.one_of(
        st.integers(min_value=1, max_value=int(roman.Standard.maximum)),
        base12_fractions(
            min_value=Fraction(roman.Standard.minimum),
            max_value=Fraction(roman.Standard.maximum),
        ),
    ),
    roman.Apostrophus: st.integers(
        min_value=int(roman.Apostrophus.minimum),
        max_value=int(roman.Apostrophus.maximum),
    ),
}

NEGATIVE_STRATEGY_CACHE: dict[type[System[Any, Any]], st.SearchStrategy] = {
    arabic.Arabic: st.one_of(
        st.integers(max_value=int(arabic.Arabic.minimum) * 2),
        st.integers(min_value=int(arabic.Arabic.maximum) * 2),
        st.floats(max_value=arabic.Arabic.minimum * 2),
        st.floats(min_value=arabic.Arabic.maximum * 2),
    ),
    egyptian.Egyptian: st.integers(max_value=int(egyptian.Egyptian.minimum) - 1),
    roman.Early: st.one_of(
        st.integers(max_value=int(roman.Early.minimum) - 1),
        st.integers(min_value=int(roman.Early.maximum) + 1),
    ),
    roman.Apostrophus: st.one_of(
        st.integers(max_value=int(roman.Apostrophus.minimum) - 1),
        st.integers(min_value=int(roman.Apostrophus.maximum) + 1),
    ),
    roman.Standard: st.one_of(
        st.integers(max_value=int(roman.Standard.minimum) - 1),
        st.integers(min_value=int(roman.Standard.maximum) + 1),
        # not base 12
        st.fractions().filter(lambda f: f.denominator not in (1, 2, 3, 4, 6, 12)),
    ),
}

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
