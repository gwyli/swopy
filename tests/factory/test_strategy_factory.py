"""
test_strategy_factory.py
------------------------
Demonstrates and tests the strategy factory against all four numeric kinds.

Run with:
    pytest test_strategy_factory.py -v
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

import pytest
from hypothesis import given

from swopy import System

from .factory import make_strategy
from .numeric_type import BaseNFraction, infer_numeric_kind


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
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = Fraction(1)
    _from_numeral_map: Mapping[str, Fraction] = {
        "one_third": Fraction(1, 3),
        "one_half": Fraction(1, 2),
        "one_quarter": Fraction(1, 4),
        "five_sixths": Fraction(5, 6),
        "one_twelfth": Fraction(1, 12),
        "seven_twelfths": Fraction(7, 12),
    }


class FractionIntSystem(System[str, Fraction | int]):
    """
    A system whose named values imply a base-12 (duodecimal) structure.
    The factory infers base=12 from the LCM of the denominators in `map`.
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(0)
    maximum: ClassVar[int | float | Fraction] = 1
    _from_numeral_map: Mapping[str, Fraction | int] = {
        "one_third": Fraction(1, 3),
        "one_half": Fraction(1, 2),
        "one_quarter": Fraction(1, 4),
        "five_sixths": Fraction(5, 6),
        "one_twelfth": Fraction(1, 12),
        "seven_twelfths": Fraction(7, 12),
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


def test_infers_base_from_simple_halves_and_quarters():
    class Base4System(System[str, Fraction]):
        minimum: ClassVar[int | float | Fraction] = Fraction(0)
        maximum: ClassVar[int | float | Fraction] = Fraction(1)
        _from_numeral_map: Mapping[str, Fraction] = {
            "half": Fraction(1, 2),
            "quarter": Fraction(1, 4),
        }

    kind = infer_numeric_kind(Base4System).pop()
    assert isinstance(kind, BaseNFraction)
    assert kind.base == 4  # noqa: PLR2004
