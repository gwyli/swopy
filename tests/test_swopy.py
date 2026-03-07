"""Tests for swopy.swop.

This module contains property-based tests using Hypothesis for main swopy API to
convert between different numeral systems.
"""

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

from .factory.factory import make_double_strategy, make_strategy

SYSTEMS: list[type[System[Any, Any]]] = list(get_all_systems().values())


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

    for strategy in make_double_strategy(from_system, to_system):
        number = data.draw(strategy)

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

    assume(from_system is not to_system)

    for strategy in make_double_strategy(from_system, to_system, falsify=True):
        number = data.draw(strategy)

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

    for encoding in system.encodings:
        number = data.draw(make_strategy(system))

        number_: Numeral = system.to_numeral(number, encode=encoding)
        result: Numeral = swop(number_, system, system)
        final: Denotation = system.from_numeral(result, encode=encoding)

        assert final == number, (
            f"Failed identity conversion for {system} with value {number}"
        )
        assert type(final) is type(number), (
            f"Type mismatch in identity conversion for {system} with value {number}"
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

    for strategy in make_double_strategy(from_system, to_system):
        number = data.draw(strategy)

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
