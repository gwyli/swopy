import math
from fractions import Fraction

from hypothesis import strategies as st


@st.composite
def base12_fractions(
    draw: st.DrawFn, min_value: Fraction, max_value: Fraction
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

    target_denominator = draw(st.sampled_from(sorted({1, 2, 3, 4, 6, 12})))

    # All unique numerators/denominators that reduce to one of our valid denominators.
    # A fraction n/d reduces to have denominator d/gcd(n,d).  The simplest approach:
    # generate every reduced fraction (p/q in lowest terms, gcd=1) where q is in our
    # set, then scale by any integer k so the actual stored fraction is (k*p)/(k*q).
    # We expose this as a Hypothesis composite strategy.

    lo = math.ceil(min_value * target_denominator)
    hi = math.floor(max_value * target_denominator)

    # Collect all valid numerators (coprime with target_denominator)
    valid_numerators = [
        p for p in range(lo, hi + 1) if math.gcd(abs(p), target_denominator) == 1
    ]

    if not valid_numerators:
        # Fall back: just return min_value (it satisfies the contract by
        # definition).  This edge case can happen when the range is very tight
        # and no coprime numerator fits.
        return min_value

    numerator = draw(st.sampled_from(valid_numerators))

    return Fraction(numerator, target_denominator)
