"""
numeric_type.py
---------------
Detects which numeric kind a System class represents and returns a
lightweight NumericKind value that the strategy builders can act on.

Detection order (first match wins):
  1. map contains Fraction values whose denominators share a common base
     → BaseNFraction(base)
  2. map contains Fraction values with no clear single base
     → PlainFraction
  3. minimum / maximum are int (and not bool)
     → Integer
  4. minimum / maximum are float
     → Float
  5. minimum / maximum are Fraction
     → PlainFraction
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from swopy import System


@dataclass(frozen=True)
class BaseNFraction:
    base: int


NumericKind = type | BaseNFraction


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def _infer_base(fractions: list[Fraction]) -> int | None:
    """
    Return the LCM of all denominators when they are all factors of that LCM,
    i.e. when the set of fractions is consistent with a single base.

    For example {1/3, 1/2, 1/4, 5/6, 1/12, 7/12} all have denominators that
    divide 12, so the base is 12.

    Returns None if no consistent base can be inferred (all denominators are 1,
    or only a single fraction exists with denominator 1).
    """
    denominators = [f.denominator for f in fractions]
    base = denominators[0]
    for d in denominators[1:]:
        base = _lcm(base, d)

    # Every denominator must divide the base (always true by LCM construction).
    # We additionally require base > 1 to distinguish from plain integers.
    if base <= 1:
        return None
    return base


def infer_numeric_kind(cls: type[System[Any, Any]]) -> set[NumericKind]:
    """Inspect a System subclass and return its NumericKind."""

    values: list[Any] = []

    types_ = cls._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    kinds: set[NumericKind] = set()

    for t in types_:
        if t is not Fraction:
            kinds.add(t)

    if Fraction in types_:
        if hasattr(cls, "_from_numeral_map"):
            mapping: Mapping[Any, Any] = cls.from_numeral_map()
            values = list(mapping.values())

            fraction_values = [v for v in values if isinstance(v, Fraction)]

            if fraction_values:
                base = _infer_base(fraction_values)
                if base is not None:
                    kinds.add(BaseNFraction(base=base))
            else:
                kinds.add(Fraction)
        else:
            kinds.add(Fraction)

    return kinds


def infer_numeric_kind1(cls: type[System[Any, Any]]) -> NumericKind:
    """Inspect a System subclass and return its NumericKind."""

    values: list[Any] = []

    if getattr(cls, "_from_numeral_map", {}):
        mapping: Mapping[Any, Any] = cls.from_numeral_map()
        values = list(mapping.values())

        fraction_values = [v for v in values if isinstance(v, Fraction)]

        if fraction_values:
            base = _infer_base(fraction_values)
            if base is not None:
                return BaseNFraction(base=base)
            return Fraction

    sample = getattr(cls, "minimum", None)

    if isinstance(sample, Fraction):
        return Fraction

    if isinstance(sample, int):
        return int

    if isinstance(sample, float):
        return float

    raise TypeError(
        f"Cannot infer numeric kind for {cls}: "
        f"minimum attribute has unsupported type {type(sample)}"
    )
