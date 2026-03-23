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
from dataclasses import dataclass, field
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
        return other is Fraction or isinstance(other, (BaseNFraction, SampledFractions))


@dataclass(frozen=True)
class SampledFractions:
    """
    A kind (type) to represent an incomplete set of fractions (e.g. {1/4, 1/3, 1/2,
    2/3}).  Compares equal to Fraction and BaseNFraction so that set operations treat
    it as "covers Fraction" — preventing Fraction from appearing in the symmetric
    difference — while its builder draws only from the exact representable set.
    """

    fractions: frozenset[Fraction] = field(default_factory=frozenset)

    def __hash__(self):
        return hash(Fraction)

    def __eq__(self, other: object):
        return other is Fraction or isinstance(other, (SampledFractions, BaseNFraction))


NumericKind = type | BaseNFraction | SampledFractions


def _lcm(a: int, b: int) -> int:
    """Lowest common multiple"""
    return abs(a * b) // math.gcd(a, b)


def _infer_base(fractions: list[Fraction]) -> int | None:
    """
    Return the LCM of all denominators when every multiple of 1/LCM in (0, 1)
    is additively reachable from the stored fractions.

    Additive systems (like Attic Greek) store only their primitive glyphs in
    the map (e.g. {1/4, 1/2}) but can represent all multiples of 1/LCM by
    combining glyphs (e.g. 3/4 = 1/2 + 1/4).  The reachable set is the
    fixed-point closure of the inputs under addition, keeping only values in
    (0, 1).

    For example {1/4, 1/2} closes to {1/4, 1/2, 3/4} — all three quarters —
    so the base is 4.  {1/4, 1/3, 1/2, 2/3} cannot reach 1/12 (the smallest
    element is 1/4 = 3/12), so None is returned.

    Args:
        fractions: A list of Fractions to assess.

    Returns:
        None if no consistent base can be inferred (all denominators are 1,
        or the additive closure is incomplete). Otherwise, returns the base.
    """
    denominators = [f.denominator for f in fractions]
    base = denominators[0]
    for d in denominators[1:]:
        base = _lcm(base, d)

    # We additionally require base > 1 to distinguish from plain integers.
    if base <= 1:
        return None

    # Close the fraction set under addition, keeping only values in (0, 1).
    reachable = set(fractions)
    changed = True
    while changed:
        changed = False
        for a in list(reachable):
            for b in fractions:
                c = a + b
                if Fraction(0) < c < Fraction(1) and c not in reachable:
                    reachable.add(c)
                    changed = True

    # Every multiple of 1/base in (0, 1) must be reachable.
    expected = {Fraction(n, base) for n in range(1, base)}
    if not expected.issubset(reachable):
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
                    # Incomplete fraction set: signal that Fraction is "covered"
                    # (preventing it from appearing in the falsifying symmetric
                    # difference) while the builder draws only the exact fractions.
                    kinds.add(SampledFractions(fractions=frozenset(fraction_values)))
            else:
                kinds.add(Fraction)
        else:
            kinds.add(Fraction)

    return kinds
