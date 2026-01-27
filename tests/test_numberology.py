from hypothesis import assume, given, strategies

from numberology import Numberology, System, TFromType, TToType, systems
from tests.helpers import SYSTEMS


@given(
    strategies.sampled_from(SYSTEMS),
    strategies.sampled_from(SYSTEMS),
    strategies.data(),
)
def test_round_trip(
    from_system: type[System[TFromType]],
    to_system: type[System[TToType]],
    data: strategies.DataObject,
):
    """
    Converting A -> B -> A should return the original value.
    """
    converter = Numberology()
    # Calculate the overlapping valid range
    min_val: int = max(from_system.minimum, to_system.minimum)
    max_val: int = min(from_system.maximum, to_system.maximum)

    # Guard against systems with no overlap
    if min_val > max_val:
        assume(False)  # Tells Hypothesis to skip this invalid combination

    number: int = data.draw(strategies.integers(min_value=min_val, max_value=max_val))

    # The integer strategy ensures we start with Arabic numerals, so first
    # convert to the source system
    source_input: TFromType = converter.convert(
        number, from_system=systems.arabic.Arabic, to_system=from_system
    )
    # Intermediate conversion
    result: TToType = converter.convert(source_input, from_system, to_system)
    # Back to start
    final: TFromType = converter.convert(result, to_system, from_system)
    # Last, convert back to Arabic to compare
    int_result: int = converter.convert(final, from_system, systems.arabic.Arabic)

    assert int_result == number


@given(strategies.sampled_from(SYSTEMS), strategies.data())
def test_identity_conversion(
    system: type[System[TFromType]], data: strategies.DataObject
):
    """
    Converting from a system to itself should return the input.
    """
    converter = Numberology()

    number = data.draw(
        strategies.integers(min_value=system.minimum, max_value=system.maximum)
    )

    number_: TFromType = system.from_int(number)

    result: TFromType = converter.convert(number_, system, system)

    integer: int = system.to_int(result)

    # If input was int and system is Arabic, it should stay int.
    # If system is Roman, convert(int) returns string, so we check equality of value.
    assert integer == number


def test_get_all_systems():
    """
    Each system in systems.__all__ should be retrievable.
    """
    converter = Numberology()
    result: dict[str, type[System[int]] | type[System[str]]] = (
        converter.get_all_systems()
    )

    assert all(issubclass(x, System) for x in result.values())
