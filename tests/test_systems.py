"""Tests for numeral system conversion modules.

This module contains property-based tests using Hypothesis for the Arabic, Egyptian,
and Roman numeral system converters. Tests verify bidirectional conversion accuracy
and validate range constraints for each numeral system.
"""

import pytest
from hypothesis import assume, given, strategies

from numberology import systems

SYSTEMS: list[str] = getattr(systems, "__all__", [])
SYSTEMS_WITHOUT_ARABIC: list[str] = [s for s in SYSTEMS if s != "Arabic"]


@pytest.mark.parametrize("module_name", SYSTEMS)
@given(strategies.data())
def test_reversibility(module_name: str, data: strategies.DataObject) -> None:
    """
    Verifies that numeral systems can be converted to their representation
    and back without loss of precision.
    """
    instance = getattr(systems, module_name)

    value = data.draw(
        strategies.integers(min_value=instance.minimum, max_value=instance.maximum)
    )

    encoded = instance.from_int(value)
    decoded = instance.to_int(encoded)

    assert decoded == value, f"Failed round-trip for {module_name} with value {value}"


@pytest.mark.parametrize("module_name", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.data())
def test_minima(module_name: str, data: strategies.DataObject) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    below the minimum valid value for the numeral system.

    Args:
        number: An integer below the minimum valid value for the numeral system.
    """

    instance = getattr(systems, module_name)

    value = data.draw(strategies.integers(max_value=instance.minimum - 1))

    with pytest.raises(ValueError):
        instance.from_int(value)


@pytest.mark.parametrize("module_name", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.data())
def test_maxima(module_name: str, data: strategies.DataObject) -> None:
    """Verifies that a ValueError is raised when attempting to convert numbers
    above the maximum valid value for the numeral system.

    Args:
        number: An integer above the maximum valid value for the numeral system.
    """

    instance = getattr(systems, module_name)

    value = data.draw(strategies.integers(min_value=instance.maximum + 1))

    # Some systems may treat values above the maximum as equivalent to the maximum.
    if instance.maximum_is_many:
        assert instance.from_int(value) == instance.from_int(instance.maximum)
    else:
        with pytest.raises(ValueError):
            instance.from_int(value)


@pytest.mark.parametrize("module_name", SYSTEMS_WITHOUT_ARABIC)
@given(strategies.text())
def test_roman_invalid_characters(module_name: str, value: str) -> None:
    """Verifies that a ValueError is raised when attempting to convert a string
    containing invalid characters for the numeral system.

    Args:
        number: A string containing invalid characters for the numeral system.
    """

    instance = getattr(systems, module_name)

    assume(not all(c.upper() in instance.to_int_ for c in value))

    with pytest.raises(ValueError):
        instance.to_int(value)
