"""Tests for numeral system conversion modules.

This module contains property-based tests using Hypothesis for the Arabic, Egyptian,
and Roman numeral system converters. Tests verify bidirectional conversion accuracy
and validate range constraints for each numeral system.
"""

import pytest
from hypothesis import assume, given, strategies

from numberology import System, TFromType
from tests.helpers import SYSTEMS, SYSTEMS_WITHOUT_ARABIC


@pytest.mark.parametrize("system", SYSTEMS)
@given(strategies.data())
def test_reversibility(
    system: type[System[TFromType]], data: strategies.DataObject
) -> None:
    """
    Verifies that numeral systems can be converted to their representation
    and back without loss of precision.
    """

    value = data.draw(
        strategies.integers(min_value=system.minimum, max_value=system.maximum)
    )

    encoded: TFromType = system.from_int(value)
    decoded: int = system.to_int(encoded)

    assert decoded == value, f"Failed round-trip for {system} with value {value}"


@pytest.mark.parametrize("system", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.data())
def test_minima(system: type[System[TFromType]], data: strategies.DataObject) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    below the minimum valid value for the numeral system.

    Args:
        number: An integer below the minimum valid value for the numeral system.
    """

    value = data.draw(strategies.integers(max_value=system.minimum - 1))

    with pytest.raises(ValueError):
        system.from_int(value)


@pytest.mark.parametrize("system", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.data())
def test_maxima(system: type[System[TFromType]], data: strategies.DataObject) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    above the maximum valid value for the numeral system.

    Args:
        number: An integer above the maximum valid value for the numeral system.
    """

    value = data.draw(strategies.integers(min_value=system.maximum + 1))

    # Some systems may treat values above the maximum as equivalent to the maximum.
    if system.maximum_is_many:
        assert system.from_int(value) == system.from_int(system.maximum)
    else:
        with pytest.raises(ValueError):
            system.from_int(value)


@pytest.mark.parametrize("system", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.text())
def test_invalid_characters(system: type[System[str]], value: str) -> None:
    """Verifies that a ValueError is raised when attempting to convert a string
    containing invalid characters for the numeral system.

    Args:
        number: A string containing invalid characters for the numeral system.
    """

    character_string: str = "".join(system.to_int_.keys())

    assume(not all(c.upper() in character_string for c in value))

    with pytest.raises(ValueError):
        system.to_int(value)
