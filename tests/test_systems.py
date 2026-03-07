"""Tests for numeral system conversion modules.

This module contains property-based tests using Hypothesis for the Arabic, Egyptian,
and Roman numeral system converters. Tests verify bidirectional conversion accuracy
and validate range constraints for each numeral system.
"""

from collections.abc import Container
from fractions import Fraction
from math import inf
from typing import Any, cast

import pytest
from hypothesis import assume, given, strategies

from swopy import Denotation, Numeral, System, get_all_systems

from .factory.factory import make_strategy
from .strategies import everything_except

SYSTEMS: list[type[System[Any, Any]]] = list(get_all_systems().values())

_INVALID_TYPE_STRATEGY_CACHE: dict[
    type[System[Numeral, Denotation]], strategies.SearchStrategy
] = {}


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
    if system not in _INVALID_TYPE_STRATEGY_CACHE:
        _INVALID_TYPE_STRATEGY_CACHE[system] = everything_except(
            excluded_types=base_types_
        )

    return _INVALID_TYPE_STRATEGY_CACHE[system]


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
        number = data.draw(make_strategy(system))

        encoded: Numeral = system.to_numeral(number, encode=encoding)
        decoded: str | int | float | Fraction = system.from_numeral(
            encoded, encode=encoding
        )

        assert decoded == number, f"Failed round-trip for {system} with value {number}"
        assert type(decoded) is type(number), (
            f"Type mismatch {system} between {decoded} and {number}."
        )


@pytest.mark.parametrize(
    "system",
    [
        x
        for x in SYSTEMS
        # Special case `System.maximum_is_many` and don't test maxima and minima if they
        # are unbounded
        if not x.maximum_is_many and not (x.minimum == -inf and x.maximum == inf)
    ],
)
@given(strategies.data())
def test_minima_and_maxima(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    below the minimum valid value or above the maximum valid value for the numeral
    system.
    """

    for encoding in system.encodings:
        number = data.draw(make_strategy(system, falsify=True))

        with pytest.raises(ValueError):
            system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", [x for x in SYSTEMS if x.maximum_is_many])
@given(strategies.data())
def test_minima_and_maxima_if_max_is_many(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    below the minimum valid value or above the maximum valid value for the numeral
    system.
    """

    for encoding in system.encodings:
        number = data.draw(make_strategy(system, falsify=True, over_max=True))

        with pytest.raises(ValueError):
            system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", [x for x in SYSTEMS if x.maximum_is_many])
@given(strategies.data())
def test_maximum_is_many(
    system: type[System[Numeral, Denotation]],
    data: strategies.DataObject,
) -> None:
    """Verifies that where the maximum of a numeral system represents "many" the
    value returned is the maximum.
    """
    for encoding in system.encodings:
        number = system.maximum * data.draw(make_strategy(system))

        assert system.to_numeral(number, encode=encoding) == system.to_numeral(
            system.maximum, encode=encoding
        )


@pytest.mark.parametrize("system", [x for x in SYSTEMS if str in x._get_base_types(0)])  # pyright: ignore[reportPrivateUsage]
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

    number = data.draw(make_strategy(system))

    for encoding in set(System.encodings) - set(system.encodings):
        with pytest.raises(ValueError):
            system.to_numeral(number, encode=encoding)


@pytest.mark.parametrize("system", [x for x in SYSTEMS if str in x._get_base_types(0)])  # pyright: ignore[reportPrivateUsage]
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

    alphabet = [
        x for x in system.from_numeral_map() if isinstance(x, str) and len(x) == 1
    ]
    numeral = data.draw(strategies.text(alphabet=alphabet))

    for encoding in set(System.encodings) - set(system.encodings):
        with pytest.raises(ValueError):
            system.from_numeral(numeral, encode=encoding)
