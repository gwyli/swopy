"""
Demonstrates and tests the strategy factory.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

import pytest
from hypothesis import given
from hypothesis.strategies import one_of

from swopy import System

from .factory import make_double_strategy, make_strategy
from .numeric_type import BaseNFraction, SampledFractions, infer_numeric_kind


class FloatSystem(System[float, float]):
    minimum: ClassVar[int | float | Fraction] = 0.0
    maximum: ClassVar[int | float | Fraction] = 1.0


class IntSystem(System[int, int]):
    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = 100


class PlainFractionSystem(System[Fraction, Fraction]):
    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = Fraction(1)


class Base12FractionSystem(System[str, Fraction]):
    """
    A system whose named values imply a base-12 (duodecimal) structure.
    The factory infers base=12 from the LCM of the denominators in `map`.
    All 11 twelfths (1/12 through 11/12) are present, so the set is complete.
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = Fraction(1)
    _from_numeral_map: Mapping[str, Fraction] = {
        "one_twelfth": Fraction(1, 12),
        "one_sixth": Fraction(1, 6),
        "one_quarter": Fraction(1, 4),
        "one_third": Fraction(1, 3),
        "five_twelfths": Fraction(5, 12),
        "one_half": Fraction(1, 2),
        "seven_twelfths": Fraction(7, 12),
        "two_thirds": Fraction(2, 3),
        "three_quarters": Fraction(3, 4),
        "five_sixths": Fraction(5, 6),
        "eleven_twelfths": Fraction(11, 12),
    }


class FractionIntSystem(System[str, Fraction | int]):
    """
    A system whose named values imply a base-12 (duodecimal) structure.
    The factory infers base=12 from the LCM of the denominators in `map`.
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = 1
    _from_numeral_map: Mapping[str, Fraction | int] = {
        "one_twelfth": Fraction(1, 12),
        "one_sixth": Fraction(1, 6),
        "one_quarter": Fraction(1, 4),
        "one_third": Fraction(1, 3),
        "five_twelfths": Fraction(5, 12),
        "one_half": Fraction(1, 2),
        "seven_twelfths": Fraction(7, 12),
        "two_thirds": Fraction(2, 3),
        "three_quarters": Fraction(3, 4),
        "five_sixths": Fraction(5, 6),
        "eleven_twelfths": Fraction(11, 12),
        "one": 1,
    }


class NarrowIntSystem(System[int, int]):
    """Used for two-system intersection tests."""

    minimum: ClassVar[int | float | Fraction] = 20
    maximum: ClassVar[int | float | Fraction] = 80


class TestFloatSystem:
    @given(make_strategy(FloatSystem))
    def test_values_in_bounds(self, value: float):
        assert FloatSystem.minimum <= value <= FloatSystem.maximum

    @given(make_strategy(FloatSystem, falsify=True))
    def test_values_out_of_bounds(self, value: float):
        assert value <= FloatSystem.minimum or value >= FloatSystem.maximum


class TestIntSystem:
    @given(make_strategy(IntSystem))
    def test_values_are_integers(self, value: int):
        assert isinstance(value, int)

    @given(make_strategy(IntSystem, falsify=True))
    def test_falsified_values_are_integers(self, value: int):
        assert isinstance(value, int)

    @given(make_strategy(IntSystem))
    def test_values_in_bounds(self, value: int):
        assert IntSystem.minimum <= value <= IntSystem.maximum

    @given(make_strategy(IntSystem, falsify=True))
    def test_values_out_of_bounds(self, value: int):
        assert value <= IntSystem.minimum or value >= IntSystem.maximum


class TestPlainFractionSystem:
    @given(make_strategy(PlainFractionSystem))
    def test_values_are_fractions(self, value: Fraction):
        assert isinstance(value, Fraction)

    @given(make_strategy(PlainFractionSystem, falsify=True))
    def test_falsified_values_are_fractions(self, value: Fraction):
        assert isinstance(value, Fraction)

    @given(make_strategy(PlainFractionSystem))
    def test_values_in_bounds(self, value: Fraction):
        assert PlainFractionSystem.minimum <= value <= PlainFractionSystem.maximum

    @given(make_strategy(PlainFractionSystem, falsify=True))
    def test_values_out_of_bounds(self, value: Fraction):
        assert (
            value <= PlainFractionSystem.minimum or value >= PlainFractionSystem.maximum
        )


class TestBase12FractionSystem:
    @given(make_strategy(Base12FractionSystem))
    def test_values_are_fractions(self, value: Fraction):
        assert isinstance(value, Fraction)

    @given(make_strategy(Base12FractionSystem))
    def test_values_in_bounds(self, value: Fraction):
        assert Base12FractionSystem.minimum <= value <= Base12FractionSystem.maximum

    @given(make_strategy(Base12FractionSystem))
    def test_denominators_divide_base(self, value: Fraction):
        """All generated fractions must have denominators that divide 12."""
        assert 12 % value.denominator == 0


class TestFractionIntSystem:
    @given(make_strategy(FractionIntSystem))
    def test_values_are_fractions_or_ints(self, value: Fraction):
        assert isinstance(value, (Fraction, int))

    @given(make_strategy(FractionIntSystem))
    def test_values_in_bounds(self, value: Fraction | int):
        assert FractionIntSystem.minimum <= value <= FractionIntSystem.maximum

    @given(make_strategy(FractionIntSystem))
    def test_denominators_divide_base(self, value: Fraction | int):
        """All generated fractions must have denominators that divide 12."""
        if isinstance(value, Fraction):
            assert 12 % value.denominator == 0


class TestTwoSystemIntersection:
    @given(make_strategy(IntSystem, NarrowIntSystem))
    def test_respects_intersection_bounds(self, value: int):
        # intersection of [0,100] and [20,80] → [20,80]
        assert NarrowIntSystem.minimum <= value <= NarrowIntSystem.maximum

    @given(make_strategy(IntSystem, NarrowIntSystem, falsify=True))
    def test_disrespects_intersection_bounds(self, value: int):
        # intersection of [0,100] and [20,80] → [20,80]
        assert value <= NarrowIntSystem.minimum or value >= NarrowIntSystem.maximum

    def test_empty_intersection_raises(self):
        class LowSystem(System[int, int]):
            minimum = 0
            maximum = 10

        class HighSystem(System[int, int]):
            minimum = 20
            maximum = 30

        with pytest.raises(ValueError, match="empty"):
            make_strategy(LowSystem, HighSystem)

        with pytest.raises(ValueError, match="empty"):
            make_strategy(LowSystem, HighSystem, falsify=True)


def test_infers_float():
    assert infer_numeric_kind(FloatSystem) == {float}


def test_infers_integer():
    assert infer_numeric_kind(IntSystem) == {int}


def test_infers_plain_fraction():
    assert infer_numeric_kind(PlainFractionSystem) == {Fraction}


def test_infers_base12_fraction():
    kind = infer_numeric_kind(Base12FractionSystem).pop()
    assert isinstance(kind, BaseNFraction)
    assert kind.base == 12  # noqa: PLR2004


class SampledASystem(System[str, Fraction]):
    """Incomplete fraction set: {1/3, 1/2} — additive closure cannot reach 1/6."""

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = Fraction(1)
    _from_numeral_map: Mapping[str, Fraction] = {
        "one_third": Fraction(1, 3),
        "one_half": Fraction(1, 2),
    }


class SampledBSystem(System[str, Fraction]):
    """Incomplete fraction set: {1/5, 1/2} — additive closure cannot reach 1/10."""

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = Fraction(1)
    _from_numeral_map: Mapping[str, Fraction] = {
        "one_fifth": Fraction(1, 5),
        "one_half": Fraction(1, 2),
    }


class TestDoubleSampledFractionsStrategy:
    """make_double_strategy with two SampledFractions systems intersects their sets."""

    def test_infers_sampled_kinds(self):
        kind_a = infer_numeric_kind(SampledASystem).pop()
        kind_b = infer_numeric_kind(SampledBSystem).pop()
        assert isinstance(kind_a, SampledFractions)
        assert isinstance(kind_b, SampledFractions)

    @given(one_of(*make_double_strategy(SampledASystem, SampledBSystem)))
    def test_values_are_intersection_of_fraction_sets(self, value: Fraction):
        # {1/3, 1/2} ∩ {1/5, 1/2} = {1/2}
        assert value == Fraction(1, 2)

    @given(one_of(*make_double_strategy(SampledASystem, SampledBSystem)))
    def test_values_in_bounds(self, value: Fraction):
        assert SampledASystem.minimum <= value <= SampledASystem.maximum


def test_infers_base_from_simple_halves_and_quarters():
    class Base4System(System[str, Fraction]):
        minimum: ClassVar[int | float | Fraction] = Fraction(0)
        maximum: ClassVar[int | float | Fraction] = Fraction(1)
        _from_numeral_map: Mapping[str, Fraction] = {
            "quarter": Fraction(1, 4),
            "half": Fraction(1, 2),
            "three_quarters": Fraction(3, 4),
        }

    kind = infer_numeric_kind(Base4System).pop()
    assert isinstance(kind, BaseNFraction)
    assert kind.base == 4  # noqa: PLR2004
