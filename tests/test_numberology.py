from typing import Any

from hypothesis import assume, given, strategies

from numberology import (
    Denotation,
    Numberology,
    Numeral,
    System,
    get_all_systems,
    systems,
)
from tests.helpers import SYSTEMS, TYPE_STRATEGY_MAP, base_types


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
        source_input: TFromNumeral = converter.convert(
            number, from_system=systems.arabic.Arabic, to_system=from_system
        )
        # Intermediate conversion
        result: TToNumeral = converter.convert(source_input, from_system, to_system)
        # Back to start
        final: TFromNumeral = converter.convert(result, to_system, from_system)
        # Last, convert back to Arabic to compare
        final_number: Numeral = converter.convert(
            final, from_system, systems.arabic.Arabic
        )

        assert final_number == number
        assert type(final_number) is type(number)


@given(strategies.sampled_from(SYSTEMS), strategies.data())
def test_identity_conversion(
    system: type[System[Numeral, Denotation]],
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

        number_: Numeral = system.to_numeral(number)

        result: Numeral = converter.convert(number_, system, system)

        final: Denotation = system.from_numeral(result)

        assert final == number
        assert type(final) is type(number)


def test_get_all_systems():
    """
    Each system in systems.__all__ should be retrievable.
    """
    result: dict[str, type[System[Any, Any]]] = get_all_systems()

    assert all(issubclass(x, System) for x in result.values())
