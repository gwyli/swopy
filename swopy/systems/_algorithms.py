"""Shared algorithm functions for numeral system conversions."""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import overload


def greedy_additive_to_numeral(number: int, numeral_map: Mapping[int, str]) -> str:
    """Convert an integer to a numeral string using greedy additive decomposition.

    Iterates the map in its defined order (largest denomination first), consuming
    as many copies of each denomination as fit, and concatenates the corresponding
    glyphs.

    Args:
        number: The Arabic number to convert.
        numeral_map: Ordered mapping from denomination values to their glyphs.

    Returns:
        The numeral string representation of ``number``.
    """
    result: str = ""
    for value, glyph in numeral_map.items():
        count, number = divmod(number, value)
        result += glyph * count
    return result


@overload
def char_sum_from_numeral(
    numeral: str,
    from_map: Mapping[str, int],
    system_name: str,
) -> int: ...


@overload
def char_sum_from_numeral(
    numeral: str,
    from_map: Mapping[str, int | Fraction],
    system_name: str,
) -> int | Fraction: ...


def char_sum_from_numeral(
    numeral: str,
    from_map: Mapping[str, int | Fraction],
    system_name: str,
) -> int | Fraction:
    """Convert a numeral string to a number by summing character values.

    Scans each character of ``numeral`` left-to-right, looks it up in
    ``from_map``, and accumulates the total.

    Args:
        numeral: The numeral string to convert.
        from_map: Mapping from individual characters to their numeric values.
        system_name: Human-readable system name used in the error message.

    Returns:
        The sum of the values of all characters in ``numeral``.

    Raises:
        ValueError: If any character is not present in ``from_map``.
    """
    total: int | Fraction = 0
    for char in numeral:
        if char not in from_map:
            raise ValueError(f"Invalid {system_name} character: {char!r}")
        total += from_map[char]
    return total


def multiplicative_additive_to_numeral(
    number: int, numeral_map: Mapping[int, str]
) -> str:
    """Convert an integer to a multiplicative-additive numeral string.

    Handles systems (e.g. Brahmi, Bakhshali) where:

    - Thousands: a unit-multiplier glyph (omitted when 1) precedes the
      1000 glyph.
    - Hundreds: a unit-multiplier glyph (omitted when 1) precedes the
      100 glyph.
    - Tens: a single dedicated decade glyph (10, 20, …, 90).
    - Ones: a single dedicated unit glyph (1–9).

    Args:
        number: The Arabic number to convert.
        numeral_map: Ordered mapping from integer values to their glyphs. Must
            contain keys for 1000, 100, each decade multiple of 10 (10–90),
            and each unit 1–9.

    Returns:
        The numeral string representation of ``number``.
    """
    result = ""

    # Thousands group: unit multiplier (omitted if 1) + thousands glyph
    thousands, number = divmod(number, 1000)
    if thousands:
        if thousands > 1:
            result += numeral_map[thousands]
        result += numeral_map[1000]

    # Hundreds group: unit multiplier (omitted if 1) + hundreds glyph
    hundreds, number = divmod(number, 100)
    if hundreds:
        if hundreds > 1:
            result += numeral_map[hundreds]
        result += numeral_map[100]

    # Tens: dedicated decade glyph
    tens, number = divmod(number, 10)
    if tens:
        result += numeral_map[tens * 10]

    # Ones: dedicated unit glyph
    if number:
        result += numeral_map[number]

    return result


def multiplicative_additive_from_numeral(
    numeral: str, from_map: Mapping[str, int], system_name: str
) -> int:
    """Convert a multiplicative-additive numeral string to an integer.

    Infers character roles from their map values:

    - unit_glyphs: value in 1–9
    - multiplier_glyphs: value in {100, 1000}
    - decade_glyphs: value in 10–90 (multiples of 10)

    Scans left-to-right:

    - Unit glyphs accumulate in a buffer.
    - Multiplier glyphs flush the buffer as a multiplier (defaulting to 1
      when empty), then reset the buffer.
    - Decade glyphs flush the buffer as additive ones first, then add the
      decade value.

    After the loop, any remaining buffer is added as ones.

    Args:
        numeral: The numeral string to convert.
        from_map: Mapping from individual glyphs to their integer values.
        system_name: Human-readable system name used in the error message.

    Returns:
        The integer value of ``numeral``.

    Raises:
        ValueError: If ``numeral`` contains an unrecognised character.
    """
    unit_glyphs = frozenset(g for g, v in from_map.items() if 1 <= v <= 9)  # noqa: PLR2004
    multiplier_glyphs = {g: v for g, v in from_map.items() if v in {100, 1000}}
    decade_glyphs = {g: v for g, v in from_map.items() if 10 <= v <= 90}  # noqa: PLR2004

    total = 0
    unit_buffer = 0

    for char in numeral:
        if char not in from_map:
            raise ValueError(f"Invalid {system_name} character: {char!r}")

        if char in unit_glyphs:
            unit_buffer += from_map[char]
        elif char in multiplier_glyphs:
            total += multiplier_glyphs[char] * max(unit_buffer, 1)
            unit_buffer = 0
        else:
            # Decade glyph: flush accumulated units as ones first
            total += unit_buffer
            unit_buffer = 0
            total += decade_glyphs[char]

    total += unit_buffer
    return total
