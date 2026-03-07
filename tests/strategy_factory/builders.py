"""
Builds and registers Hypothesis strategies for the test harness.

One StrategyBuilder instance per NumericKind (int, float etc.). Each builder receives
resolved (minimum, maximum) bounds and returns a Hypothesis SearchStrategy.

To add support for a new numeric kind (see numeric_type.py):

  1. Create a subclass of StrategyBuilder.
  2. Register it via @register_builder(YourKindClass).
"""

import math
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Any

from hypothesis import assume
from hypothesis import strategies as st

from .numeric_type import BaseNFraction, NumericKind


class StrategyBuilder[TNumeric: NumericKind](ABC):
    """Produce a Hypothesis strategy for a given NumericKind and bounds."""

    @abstractmethod
    def build(
        self,
        kind: TNumeric,
        minimum: Any,
        maximum: Any,
    ) -> st.SearchStrategy: ...


_REGISTRY: dict[NumericKind, StrategyBuilder[Any]] = {}


def register_builder(kind: NumericKind):
    """Class decorator - registers a StrategyBuilder for a NumericKind type.

    Args:
        kind: The type (int, float etc.) to associate this StrategyBuilder to.
        Each kind must be unique.
    Returns:
        A decorator to register a StrategyBuilder class
    """

    def decorator(
        builder_cls: type[StrategyBuilder[Any]],
    ) -> type[StrategyBuilder[Any]]:
        _REGISTRY[kind] = builder_cls()
        return builder_cls

    return decorator


def get_builder(kind: NumericKind) -> StrategyBuilder[Any]:
    """Gets a StrategyBuilder instance to create strategies. Called in factory.py

    Args:
        kind: The type (int, float etc.) of StrategyBuilder to return.

    Returns:
        The appropritate StrategyBuilder instance for the kind
    """
    key = kind if isinstance(kind, type) else type(kind)
    builder = _REGISTRY.get(key)
    if builder is None:
        raise NotImplementedError(
            f"No StrategyBuilder registered for {type(kind).__name__}. "
            "Register one with @register_builder."
        )
    return builder


@register_builder(float)
class FloatStrategyBuilder(StrategyBuilder[Any]):
    def build(
        self,
        kind: float,  # noqa: ARG002
        minimum: float | None = None,
        maximum: float | None = None,
    ) -> st.SearchStrategy:
        # `System.minimum: Fraction = Fraction(1, 12)` results in the error:
        # min_value=Fraction(1, 12) cannot be exactly represented as a float of width 64
        # Force `System.minimum` and `System.maximum` to be flots when generating the
        # strategy
        lo = float(minimum) if minimum is not None else None
        hi = float(maximum) if maximum is not None else None
        return st.floats(min_value=lo, max_value=hi, allow_nan=False)


@register_builder(int)
class IntegerStrategyBuilder(StrategyBuilder[Any]):
    def build(
        self,
        kind: int,  # noqa: ARG002
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> st.SearchStrategy:
        # If `System.minimum: Fraction = Fraction(1, 3)` then
        # `int(System.minimum) = 0 < System.minimum`, and the reverse for System.maximum
        # ensure that `System.minimum < number < System.maximum`.
        lo = math.ceil(minimum) if minimum is not None else None
        hi = math.floor(maximum) if maximum is not None else None
        return st.integers(min_value=lo, max_value=hi)


@register_builder(Fraction)
class FractionStrategyBuilder(StrategyBuilder[Any]):
    def build(
        self,
        kind: Fraction,  # noqa: ARG002
        minimum: Fraction | None = None,
        maximum: Fraction | None = None,
    ) -> st.SearchStrategy:
        return st.fractions(min_value=minimum, max_value=maximum)


@register_builder(BaseNFraction)
class BaseNFractionStrategyBuilder(StrategyBuilder[Any]):
    """
    Generates fractions whose denominators are factors of `kind.base`.

    Strategy: pick a denominator d that divides `base`, then pick a
    numerator n such that minimum ≤ n/d ≤ maximum.
    """

    def build(
        self,
        kind: BaseNFraction,
        minimum: Fraction | None = None,
        maximum: Fraction | None = None,
    ) -> st.SearchStrategy:

        if not minimum and not maximum:
            raise ValueError(
                "Both minimum and maximum must be passed to base N fraction builders"
            )

        base = kind.base
        valid_denominators = [d for d in range(1, base + 1) if base % d == 0]

        @st.composite
        def _strategy(draw: st.DrawFn):
            denominator = draw(st.sampled_from(valid_denominators))
            min_numerator = (
                math.ceil(minimum * denominator) if minimum is not None else None
            )
            max_numerator = (
                math.floor(maximum * denominator) if maximum is not None else None
            )
            if (
                min_numerator is not None
                and max_numerator is not None
                and min_numerator > max_numerator
            ):
                # This denominator yields no valid fractions in range; filter.
                assume(False)

            numerator = draw(
                st.integers(min_value=min_numerator, max_value=max_numerator)
            )
            assume(numerator // denominator != numerator / denominator)

            return Fraction(numerator, denominator)

        return _strategy()
