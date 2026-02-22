"""Tests for swopy.swop.

This module contains property-based tests using Hypothesis for main swopy API to
convert between different numeral systems.
"""

from fractions import Fraction
from math import ceil
from typing import Any

import pytest
from hypothesis import assume, given, strategies

from swopy import (
    Denotation,
    Numeral,
    System,
    get_all_systems,
    swop,
    systems,
)
from tests.helpers import SYSTEMS, TYPE_STRATEGY_MAP, min_max


@given(
    strategies.sampled_from(SYSTEMS),
    strategies.sampled_from(SYSTEMS),
    strategies.data(),
)
def test_round_trip[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]],
    data: strategies.DataObject,
):
    """
    Converting A -> B -> A should return the original value.
    """
    # Calculate the overlapping valid range
    min_val = min_max(max, from_system.minimum, to_system.minimum)
    max_val = min_max(min, from_system.maximum, to_system.maximum)

    # Guard against systems with no overlap
    if min_val > max_val:
        assume(False)

    to_base_types: tuple[type] = to_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(to_base_types) >= 1, "System must have at least one base type"

    from_base_types: tuple[type] = from_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(from_base_types) >= 1, "System must have at least one base type"

    for base_type in set(from_base_types) & set(to_base_types):
        kwargs: dict[str, int] = {
            "min_value": min_val,
            "max_value": max_val,
        }

        if base_type is Fraction:
            kwargs["max_denominator"] = 12

        number = data.draw(TYPE_STRATEGY_MAP[base_type](**kwargs))
        if isinstance(number, Fraction):
            assume(number.denominator // 12 == number.denominator / 12)
            if number.denominator == 1:
                number = int(number)

        # We always start with a numeric strategy, so first convert to from_system
        # from Arabic numerals
        source_input: TFromNumeral = swop(
            number, from_system=systems.arabic.Arabic, to_system=from_system
        )
        # Intermediate conversion
        result: TToNumeral = swop(source_input, from_system, to_system)
        # Back to start
        final: TFromNumeral = swop(result, to_system, from_system)
        # Last, convert back to Arabic to compare
        final_number: Numeral = swop(final, from_system, systems.arabic.Arabic)

        assert final_number == number, (
            f"{number} incorrectly converted to {final_number}."
        )

        assert type(final_number) is type(number), (
            f"{number} is not of the same type as {final_number}"
        )


@given(
    strategies.sampled_from(SYSTEMS),
    strategies.sampled_from(SYSTEMS),
    strategies.data(),
)
def test_round_trip_failure[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]],
    data: strategies.DataObject,
):
    """
    Converting A -> B -> A should raise a TypeError if the systems have no overlapping
    valid types.
    """
    # Calculate the overlapping valid range
    min_val = min_max(max, from_system.minimum, to_system.minimum)
    max_val = min_max(min, from_system.maximum, to_system.maximum)

    # Guard against systems with no overlap
    if min_val > max_val:
        assume(False)

    to_base_types: tuple[type] = to_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(to_base_types) >= 1, "System must have at least one base type"

    from_base_types: tuple[type] = from_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(from_base_types) >= 1, "System must have at least one base type"

    for base_type in set(from_base_types) ^ set(to_base_types):
        number = data.draw(
            TYPE_STRATEGY_MAP[base_type](min_value=min_val, max_value=max_val)
        )

        # If a generated fraction is an int no type error should be raised when
        # converting between two int compatible systems
        if isinstance(number, Fraction):
            assume(int(number) != number)

            assume(number.denominator in (2, 3, 4, 6))

        with pytest.raises(TypeError):
            # We always start with a numeric strategy, so first convert to from_system
            # from Arabic numerals
            source_input: TFromNumeral = swop(
                number, from_system=systems.arabic.Arabic, to_system=from_system
            )
            swop(source_input, from_system, to_system)


@given(strategies.sampled_from(SYSTEMS), strategies.data())
def test_identity_conversion(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
):
    """
    Converting from a system to itself should return the input.
    """
    base_types: tuple[type] = system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]

    assert len(base_types) >= 1, "System must have at least one base type"

    for encoding in system.encodings:
        for base_type in base_types:
            kwargs: dict[str, int | float | Fraction] = {
                "min_value": ceil(system.minimum),
                "max_value": system.maximum,
            }

            if base_type is Fraction:
                kwargs["max_denominator"] = 12

            number = data.draw(TYPE_STRATEGY_MAP[base_type](**kwargs))

            # Roman numerals only supported base-12 fractions
            if isinstance(number, Fraction) and system.__name__ == "Standard":
                assume(number.denominator in (2, 3, 4, 6))

            number_: Numeral = system.to_numeral(number, encode=encoding)
            result: Numeral = swop(number_, system, system)
            final: Denotation = system.from_numeral(result, encode=encoding)

            assert final == number, (
                "Failed identity conversion for {system} with value {number}"
            )
            assert type(final) is type(number), (
                "Type mismatch in identity conversion for {system} with value {number}"
            )


def test_get_all_systems():
    """
    Each system in systems.__all__ should be retrievable.
    """
    result: dict[str, type[System[Any, Any]]] = get_all_systems()

    assert all(issubclass(x, System) for x in result.values())
    assert len(result) > 0, "No systems found. Ensure systems.__all__ is populated."


@given(
    strategies.sampled_from(SYSTEMS),
    strategies.sampled_from(SYSTEMS),
    strategies.data(),
)
def test_encodings[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]],
    data: strategies.DataObject,
):
    """
    Verifies that a value error is raised when an encoding which both
    numeral systems don't support is used.
    """

    # Calculate the overlapping valid range
    min_val = min_max(max, from_system.minimum, to_system.minimum)
    max_val = min_max(min, from_system.maximum, to_system.maximum)

    # Guard against systems with no overlap
    if min_val > max_val:
        assume(False)

    to_base_types: tuple[type] = to_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(to_base_types) >= 1, "System must have at least one base type"

    from_base_types: tuple[type] = from_system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(from_base_types) >= 1, "System must have at least one base type"

    for base_type in set(from_base_types) & set(to_base_types):
        kwargs: dict[str, int | float | Fraction] = {
            "min_value": ceil(from_system.minimum),
            "max_value": from_system.maximum,
        }

        if base_type is Fraction:
            kwargs["max_denominator"] = 12

        number = data.draw(TYPE_STRATEGY_MAP[base_type](**kwargs))

        # Roman numerals only supported base-12 fractions
        if isinstance(number, Fraction) and from_system.__name__ == "Standard":
            assume(number.denominator in (2, 3, 4, 6))

        # We always start with a numeric strategy, so first convert to from_system
        # from Arabic numerals
        source_input: TFromNumeral = swop(
            number, from_system=systems.arabic.Arabic, to_system=from_system
        )

        for encoding in from_system.encodings:
            if encoding not in to_system.encodings:
                with pytest.raises(ValueError):
                    swop(source_input, from_system, to_system, encode=encoding)

        for encoding in to_system.encodings:
            if encoding not in from_system.encodings:
                with pytest.raises(ValueError):
                    swop(source_input, from_system, to_system, encode=encoding)
