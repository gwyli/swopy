"""
factory.py
----------
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

from typing import Any

from hypothesis.strategies import SearchStrategy, one_of

from swopy import Denotation, Numeral, System

from . import builders
from .numeric_type import infer_numeric_kind


def _resolve_bounds[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    cls_a: type[System[TFromNumeral, TFromDenotation]],
    cls_b: type[System[TToNumeral, TToDenotation]] | None,
) -> tuple[Denotation, Denotation]:
    """
    Single class  → (cls_a.minimum, cls_a.maximum)
    Two classes   → (max of minimums, min of maximums)

    Raises ValueError when the intersection is empty.
    """
    lo = cls_a.minimum
    hi = cls_a.maximum

    if cls_b is not None:
        lo = max(lo, cls_b.minimum)
        hi = min(hi, cls_b.maximum)

    if lo > hi:
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
    cls_a: type[System[TFromNumeral, TFromDenotation]],
    cls_b: type[System[TToNumeral, TToDenotation]] | None = None,
    falsify: bool = False,
    over_max: bool = False,
) -> SearchStrategy:
    """
    Build a Hypothesis strategy appropriate for the numeric type of *cls_a*,
    constrained to the intersection of bounds when *cls_b* is supplied.

    Parameters
    ----------
    cls_a:
        The primary System class.  Its numeric type (float, int, Fraction,
        or base-N fraction) determines which strategy is generated.
    cls_b:
        An optional second System class.  When provided the lower bound
        becomes max(cls_a.minimum, cls_b.minimum) and the upper bound
        becomes min(cls_a.maximum, cls_b.maximum).
    over_max:
        indicates that we're trying to test above the maximum for a class
        where maximum_is_many

    Returns
    -------
    hypothesis.strategies.SearchStrategy
    """
    if over_max and not cls_a.maximum_is_many:
        raise ValueError(
            "over_max can only be used when the system defines the maximum as many"
        )

    kinds = infer_numeric_kind(cls_a)
    if cls_b is not None:
        kinds.intersection(infer_numeric_kind(cls_b))

    builders_: list[SearchStrategy[Any]] = []

    for kind in kinds:
        lo, hi = _resolve_bounds(cls_a, cls_b)

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
            builders_.append(builder.build(kind, hi + 1, None))
            builders_.append(builder.build(kind, None, lo - 1))
        # Or where a high number results in a lower number being returned
        else:
            builders_.append(builder.build(kind, None, lo - 1))

    return one_of(*builders_)


def make_double_strategy[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    cls_a: type[System[TFromNumeral, TFromDenotation]],
    cls_b: type[System[TToNumeral, TToDenotation]],
    falsify: bool = False,
) -> list[SearchStrategy[Any]]:

    if not falsify:
        kinds = infer_numeric_kind(cls_a) & infer_numeric_kind(cls_b)
    else:
        kinds = infer_numeric_kind(cls_a) ^ infer_numeric_kind(cls_b)

    builders_: list[SearchStrategy[Any]] = []

    for kind in kinds:
        lo, hi = _resolve_bounds(cls_a, cls_b)

        builder = builders.get_builder(kind)
        builders_.append(builder.build(kind, lo, hi))

    return builders_
