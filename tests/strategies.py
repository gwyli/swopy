import math
from fractions import Fraction
from types import UnionType
from typing import Any

from hypothesis import strategies as st


@st.composite
def baseN_fractions(
    draw: st.DrawFn,
    base: int,
    min_value: Fraction,
    max_value: Fraction,
) -> Fraction:
    """
    A Hypothesis composite strategy that draws a fraction whose reduced form
    has a denominator in {1, 2, 3, 4, 6, 12}.

    Args:
        min_value: The inclusive lower bound.
        max_value: The inclusive upper bound.
    """
    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) must be <= max_value ({max_value})")

    possible_denominators = {x for x in range(2, base + 1) if base // x == base / x}

    target_denominator = draw(st.sampled_from(sorted(possible_denominators)))

    # All unique numerators/denominators that reduce to one of our valid denominators.
    # A fraction n/d reduces to have denominator d/gcd(n,d).  The simplest approach:
    # generate every reduced fraction (p/q in lowest terms, gcd=1) where q is in our
    # set, then scale by any integer k so the actual stored fraction is (k*p)/(k*q).
    # We expose this as a Hypothesis composite strategy.

    lo = math.ceil(min_value * target_denominator)
    hi = math.floor(max_value * target_denominator)

    # Collect all valid numerators (coprime with target_denominator)
    valid_numerators = [
        p
        for p in range(lo, hi + 1)
        if math.gcd(abs(p), target_denominator) == 1
        # Don't generate ints as Fractions
        and p // target_denominator != p / target_denominator
    ]

    if not valid_numerators:
        # Fall back: just return min_value (it satisfies the contract by
        # definition).  This edge case can happen when the range is very tight
        # and no coprime numerator fits.
        return min_value

    numerator = draw(st.sampled_from(valid_numerators))

    return Fraction(numerator, target_denominator)


def everything_except(
    excluded_types: tuple[type | UnionType, ...],
) -> st.SearchStrategy[Any]:
    """Generate arbitrary values excluding instances of specified types.

    Args:
        excluded_types: A type or tuple of types to exclude from generation.

    Returns:
        A strategy that generates values not matching the excluded type(s).
    """
    return (
        st.from_type(object)
        .map(type)
        .filter(lambda x: not isinstance(x, excluded_types))
    )
