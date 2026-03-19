"""
Detects which numeric kind (int, float, etc.) a System class represents and returns a
lightweight NumericKind value that the strategy builders can act on.

In addition to standard Python types can be used to create new types, e.g. a Fraction of
base N.

To create a new type if required by a system:

  1. Create a new frozen dataclass to represent the type
  2. If the type shadows a standard Python type implement __hash__ and __eq__ in a
     manner which indicates they are the same type
  3. Add the dataclass to the NumericKind declaration
  4. Modify infer_numeric_kind() to detect and add this type.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from swopy import System


@dataclass(frozen=True)
class BaseNFraction:
    """
    A kind (type) to represent fractions of base N.
    """

    base: int

    def __hash__(self):
        return hash(Fraction)

    def __eq__(self, other: object):
        return other is Fraction or isinstance(other, BaseNFraction)


NumericKind = type | BaseNFraction


def _lcm(a: int, b: int) -> int:
    """Lowest common multiple"""
    return abs(a * b) // math.gcd(a, b)


def _infer_base(fractions: list[Fraction]) -> int | None:
    """
    Return the LCM of all denominators when they are all factors of that LCM,
    i.e. when the set of fractions is consistent with a single base.

    For example {1/3, 1/2, 1/4, 5/6, 1/12, 7/12} all have denominators that
    divide 12, so the base is 12.

    Args:
        fractions: A list of Fractions to assess.

    Returns:
        None if no consistent base can be inferred (all denominators are 1,
        or only a single fraction exists with denominator 1). Otherwise, returns
        the base of the list of fractions.
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


def infer_numeric_kind(system: type[System[Any, Any]]) -> set[NumericKind]:
    """Inspect a System subclass and return its NumericKind.

    Args:
        system: The system to be assessed

    Returns:
        The set of kinds (types) associated with the system.
    """

    values: list[Any] = []

    types_ = system._denotation_runtime_type  # pyright: ignore[reportPrivateUsage]
    kinds: set[NumericKind] = set()

    for t in types_:
        if t is not Fraction:
            kinds.add(t)

    if Fraction in types_:
        if hasattr(system, "_from_numeral_map"):
            mapping: Mapping[Any, Any] = system.from_numeral_map()
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
