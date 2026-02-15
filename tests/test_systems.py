"""Tests for numeral system conversion modules.

This module contains property-based tests using Hypothesis for the Arabic, Egyptian,
and Roman numeral system converters. Tests verify bidirectional conversion accuracy
and validate range constraints for each numeral system.
"""

from collections.abc import Container
from fractions import Fraction
from sys import float_info

import pytest
from hypothesis import assume, given, strategies

from swopy import Denotation, Numeral, System
from tests.helpers import (
    SYSTEMS,
    SYSTEMS_WITHOUT_ARABIC,
    TYPE_STRATEGY_MAP,
    everything_except,
)


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_reversibility(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """
    Verifies that numeral systems can be converted to their representation
    and back without loss of precision.
    """
    base_types: tuple[type] = system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]

    assert len(base_types) >= 1, "System must have at least one base type"

    for encoding in system.encodings:
        for base_type in base_types:
            number = data.draw(
                TYPE_STRATEGY_MAP[base_type](
                    min_value=system.minimum, max_value=system.maximum
                )
            )

            encoded: Numeral = system.to_numeral(number, encode=encoding)
            decoded: str | int | float | Fraction = system.from_numeral(
                encoded, encode=encoding
            )

            assert decoded == number, (
                f"Failed round-trip for {system} with value {number}"
            )


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_minima(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    below the minimum valid value for the numeral system.
    """
    base_types: tuple[type] = system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]

    assert len(base_types) >= 1, "System must have at least one base type"

    for encoding in system.encodings:
        for base_type in base_types:
            number = data.draw(
                TYPE_STRATEGY_MAP[base_type](max_value=system.minimum - 1)
            )

            # For unbounded systems adding 1 is not enough to exceed the bound
            if system.maximum == float_info.max:
                number = number * 2

            with pytest.raises(ValueError):
                system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_maxima(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    above the maximum valid value for the numeral system.
    """
    base_types: tuple[type] = system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]

    assert len(base_types) >= 1, "System must have at least one base type"

    for encoding in system.encodings:
        for base_type in base_types:
            number = data.draw(
                TYPE_STRATEGY_MAP[base_type](min_value=system.maximum + 1)
            )

            # For unbounded systems adding 1 is not enough to exceed the bound
            if system.maximum == float_info.max:
                number = number * 2

            # Some systems may treat values above the maximum as equivalent to the
            # maximum.
            if system.maximum_is_many:
                assert system.to_numeral(number, encode=encoding) == system.to_numeral(
                    system.maximum, encode=encoding
                )
            else:
                with pytest.raises(ValueError):
                    system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.text())
def test_invalid_characters(system: type[System[str, Denotation]], value: str) -> None:
    """Verifies that a ValueError is raised when attempting to convert a string
    containing invalid characters for the numeral system.
    """

    character_string: str = "".join(system.from_numeral_map.keys())

    assume(not all(c.upper() in character_string for c in value))

    for encoding in system.encodings:
        with pytest.raises(ValueError):
            system.from_numeral(value, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_invalid_denotations(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert a number
    of an invalid type for the numeral system.
    """

    base_types: Container[type] = tuple(system._get_base_types(1))  # pyright: ignore[reportPrivateUsage]
    assert len(base_types) >= 1, "System must have at least one base type"

    number = data.draw(everything_except(excluded_types=base_types))

    for encoding in system.encodings:
        with pytest.raises(TypeError):
            system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_invalid_numerals(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert a number
    of an invalid type for the numeral system.
    """

    base_types: Container[type] = tuple(system._get_base_types(0))  # pyright: ignore[reportPrivateUsage]
    assert len(base_types) >= 1, "System must have at least one base type"

    number = data.draw(everything_except(excluded_types=base_types))

    for encoding in system.encodings:
        with pytest.raises(TypeError):
            system.from_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_invalid_encodings_to_numeral(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to use an
    invalid encoding when converting to a numeral.
    """

    base_types: Container[type] = system._get_base_types(1)  # pyright: ignore[reportPrivateUsage]
    assert len(base_types) >= 1, "System must have at least one base type"

    for base_type in base_types:
        number = data.draw(
            TYPE_STRATEGY_MAP[base_type](
                min_value=system.minimum, max_value=system.maximum
            )
        )

        for encoding in System.encodings:
            if encoding not in system.encodings:
                with pytest.raises(ValueError):
                    system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.data())
def test_invalid_encodings_from_numeral(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to use an
    invalid encoding when converting from a numeral system.

    Args:
        number: A valid number for the numeral system.
    """

    base_types: Container[type] = system._get_base_types(0)  # pyright: ignore[reportPrivateUsage]
    assert len(base_types) >= 1, "System must have at least one base type"

    alphabet = [x for x in system.from_numeral_map if len(x) == 1]
    numeral = data.draw(strategies.text(alphabet=alphabet))

    for encoding in System.encodings:
        if encoding not in system.encodings:
            with pytest.raises(ValueError):
                system.from_numeral(numeral, encode=encoding)
