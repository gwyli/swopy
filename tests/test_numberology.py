from typing import Any

from hypothesis import assume, given, strategies

from numberology import (
    Numberology,
    RealNumber,
    System,
    TFromType,
    TToType,
    get_all_systems,
    systems,
)
from tests.helpers import SYSTEMS, TYPE_STRATEGY_MAP, base_types


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
    min_val = max(from_system.minimum, to_system.minimum)
    max_val = min(from_system.maximum, to_system.maximum)

    # Guard against systems with no overlap
    if min_val > max_val:
        assume(False)

    for base_type in base_types(from_system):
        assume(base_type in base_types(to_system))

        number = data.draw(
            TYPE_STRATEGY_MAP[base_type](min_value=min_val, max_value=max_val)
        )

        # We always start with a numeric strategy, so first convert to from_system
        # from Arabic numerals
        source_input: TFromType = converter.convert(
            number, from_system=systems.arabic.Arabic, to_system=from_system
        )
        # Intermediate conversion
        result: TToType = converter.convert(source_input, from_system, to_system)
        # Back to start
        final: TFromType = converter.convert(result, to_system, from_system)
        # Last, convert back to Arabic to compare
        int_result: RealNumber = converter.convert(
            final, from_system, systems.arabic.Arabic
        )

        assert int_result == number


@given(strategies.sampled_from(SYSTEMS), strategies.data())
def test_identity_conversion(
    system: type[System[TFromType]],
    data: strategies.DataObject,
):
    """
    Converting from a system to itself should return the input.
    """
    converter = Numberology()
    for base_type in base_types(system):
        number = data.draw(
            TYPE_STRATEGY_MAP[base_type](
                min_value=system.minimum, max_value=system.maximum
            )
        )

        number_: TFromType = system.from_int(number)

        result: TFromType = converter.convert(number_, system, system)

        integer: RealNumber = system.to_int(result)

        assert integer == number


def test_get_all_systems():
    """
    Each system in systems.__all__ should be retrievable.
    """
    result: dict[str, type[System[Any]]] = get_all_systems()

    assert all(issubclass(x, System) for x in result.values())
