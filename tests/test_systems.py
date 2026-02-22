"""Tests for numeral system conversion modules.

This module contains property-based tests using Hypothesis for the Arabic, Egyptian,
and Roman numeral system converters. Tests verify bidirectional conversion accuracy
and validate range constraints for each numeral system.
"""

from collections.abc import Container
from fractions import Fraction
from math import ceil
from sys import float_info
from typing import cast

import pytest
from hypothesis import HealthCheck, assume, given, settings, strategies

from swopy import Denotation, Numeral, System
from tests.helpers import (
    SYSTEMS,
    SYSTEMS_WITHOUT_ARABIC,
    TYPE_STRATEGY_MAP,
    everything_except,
)

_STRATEGY_CACHE: dict[type[System[Numeral, Denotation]], strategies.SearchStrategy] = {}


def load_strategies(
    system: type[System[Numeral, Denotation]], base_types: Container[type]
):
    """
    When running everything_except Hypothesis was refiltering the list of strategies on
    each call. Caching the list of strategies on a per system basis removes 12s (50%) of
    the execution time from Python 3.13 tests and 2s (16%) from Python 3.14+, likely due
    to Python 3.14s tail-call optimisations.
    """
    base_types_: tuple[type] = cast(tuple[type], base_types)
    if system not in _STRATEGY_CACHE:
        _STRATEGY_CACHE[system] = everything_except(excluded_types=base_types_)

    return _STRATEGY_CACHE[system]


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
@settings(suppress_health_check=[HealthCheck.filter_too_much])
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
            kwargs: dict[str, int | float | Fraction] = {
                "min_value": ceil(system.minimum),
                "max_value": system.maximum,
            }

            if base_type is Fraction:
                kwargs["max_denominator"] = 12

            number = data.draw(TYPE_STRATEGY_MAP[base_type](**kwargs))

            # Roman numerals only supported base-12 fractions
            if isinstance(number, Fraction) and system.__name__ == "Standard":
                assume(number.denominator in (2, 3, 4, 6, 12))

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
            if system.minimum == -float_info.max:
                min_val = system.minimum
            else:
                min_val = ceil(system.minimum)

            number = data.draw(TYPE_STRATEGY_MAP[base_type](max_value=min_val - 1))

            # For unbounded systems adding 1 is not enough to exceed the bound
            #
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

    character_string: str = "".join(system.from_numeral_map().keys())

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

    number = data.draw(load_strategies(system, base_types))

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

    number = data.draw(load_strategies(system, base_types))

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
                min_value=ceil(system.minimum), max_value=system.maximum
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

    alphabet = [
        x for x in system.from_numeral_map() if isinstance(x, str) and len(x) == 1
    ]
    numeral = data.draw(strategies.text(alphabet=alphabet))

    for encoding in System.encodings:
        if encoding not in system.encodings:
            with pytest.raises(ValueError):
                system.from_numeral(numeral, encode=encoding)
