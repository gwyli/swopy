"""
Public API for the strategy factory.

Usage
-----
    from factory import make_strategy

    # Single system
    strategy = make_strategy(MySystem)

    # Two systems - bounds are intersected
    strategy = make_strategy(SystemA, SystemB)

    # Use in a test
    @given(make_strategy(MySystem))
    def test_something(value):
        ...
"""

from fractions import Fraction
from math import inf
from typing import Any

from hypothesis.strategies import SearchStrategy, one_of

from swopy import Denotation, Numeral, System

from . import builders
from .numeric_type import BaseNFraction, infer_numeric_kind


def _resolve_bounds[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]] | None,
    falsify: bool = False,
) -> tuple[Denotation | None, Denotation | None]:
    """
    Resolves the bounds between two systems to enable building a working or failing
    strategy.

    Single class  → (from_system.minimum, from_system.maximum)
    Two classes   → (max of minimums, min of maximums)

    Args:
        from_system: The system being converted from.
        to_system: The system being converted to, or None.
        falsify: If the test is designed to fail produce bounds to help this.

    Returns:
        A tuple of bounds that will succeed or fail. Where either the minima or maxima
        is unbounded they will be None.

    Raises:
        ValueError when the intersection is empty.
    """
    lo = from_system.minimum
    hi = from_system.maximum

    if to_system is not None:
        lo = max(lo, to_system.minimum)
        hi = min(hi, to_system.maximum)

    # If we're falsifying the bound then ensure
    # we're outside it
    if falsify:
        lo = lo - 1
        hi = hi + 1

    # Hypothesis maps unbounded min/max to None
    if lo == -inf:
        lo = None
    if hi == inf:
        hi = None

    if lo and hi and lo > hi:
        raise ValueError(
            f"Resolved bounds [{lo}, {hi}] are empty. "
            "The two systems have no overlapping range."
        )

    return lo, hi


def make_strategy[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]] | None = None,
    falsify: bool = False,
    over_max: bool = False,
) -> SearchStrategy:
    """
    Build a Hypothesis strategy appropriate for the numeric type of from_system*,
    constrained to the intersection of bounds when to_system* is supplied.

    Args:
        from_system: The primary System class. Its numeric type (float, int, Fraction,
            base-N fraction etc.) determines which strategy is generated.
        to_system: An optional second System class. When provided, is used to determine
            bounds for the strategies of from_system.
        falsify: Is the test designed to fail?
        over_max: indicates that we're trying to test above the maximum for a class
            where maximum_is_many

    Returns:
        A Hypothesis SearchStrategy for all valid types for the System
    """
    if over_max and not from_system.maximum_is_many:
        raise ValueError(
            "over_max can only be used when the system defines the maximum as many"
        )

    kinds = infer_numeric_kind(from_system)

    builders_: list[SearchStrategy[Any]] = []

    for kind in kinds:
        lo, hi = _resolve_bounds(from_system, to_system, falsify)

        builder = builders.get_builder(kind)

        # Expected success
        if not falsify:
            # Where bounds result in the exact number being returned
            if not over_max:
                builders_.append(builder.build(kind, lo, hi))
            # Or where a high number results in a lower number being returned
            else:
                builders_.append(builder.build(kind, lo, None))

        # Otherwise, an expected success
        # where bounds result in the exact number being returned
        elif not over_max:
            builders_.append(builder.build(kind, hi, None))
            builders_.append(builder.build(kind, None, lo))
        # Or where a high number results in a lower number being returned
        else:
            builders_.append(builder.build(kind, None, lo))

    return one_of(*builders_)


def make_double_strategy[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]],
    falsify: bool = False,
) -> list[SearchStrategy[Any]]:
    """
    Build a Hypothesis strategy that's (in)appropriate for the types of from_system
    and to_system, constrained to the intersection of the minimum and maximum of the two
    systems.

    Args:
        from_system: The source numeral system.
        to_system: The target numeral system.
        falsify: Is the test designed to fail?

    Returns:
        A Hypothesis SearchStrategy for all (in)valid types for the Systems
    """
    if not falsify:
        from_kinds = infer_numeric_kind(from_system)
        to_kinds = infer_numeric_kind(to_system)
        kinds = from_kinds & to_kinds
        frac_bases = [
            k.base for k in (*from_kinds, *to_kinds) if isinstance(k, BaseNFraction)
        ]
        if frac_bases:
            min_base = min(frac_bases)
            compatible = all(base % min_base == 0 for base in frac_bases)
            resolved: set[BaseNFraction | type] = set()
            for k in kinds:
                if isinstance(k, BaseNFraction) or k is Fraction:
                    if compatible:
                        resolved.add(BaseNFraction(min_base))
                else:
                    resolved.add(k)
            kinds = resolved
    else:
        kinds = infer_numeric_kind(from_system) ^ infer_numeric_kind(to_system)

    builders_: list[SearchStrategy[Any]] = []

    for kind in kinds:
        lo, hi = _resolve_bounds(from_system, to_system)

        builder = builders.get_builder(kind)
        builders_.append(builder.build(kind, lo, hi))

    return builders_
