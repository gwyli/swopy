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


def reversed_greedy_additive_to_numeral(
    number: int, numeral_map: Mapping[int, str]
) -> str:
    """Convert an integer to a right-to-left numeral string.

    Uses greedy additive decomposition (see ``greedy_additive_to_numeral``) then
    reverses the result so that the highest-denomination glyph appears rightmost,
    matching writing systems that read right-to-left (e.g. Etruscan).

    Args:
        number: The Arabic number to convert.
        numeral_map: Ordered mapping from denomination values to their glyphs.

    Returns:
        The numeral string representation of ``number``, with glyphs in
        right-to-left order (largest denomination rightmost).
    """
    return greedy_additive_to_numeral(number, numeral_map)[::-1]


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


def reversed_char_sum_from_numeral(
    numeral: str,
    from_map: Mapping[str, int],
    system_name: str,
) -> int:
    """Convert a right-to-left numeral string to a number by summing character values.

    Reverses ``numeral`` before processing, so that right-to-left writing systems
    (e.g. Etruscan) can be parsed with the same character-sum logic used for
    left-to-right systems.

    Args:
        numeral: The numeral string to convert (in right-to-left display order).
        from_map: Mapping from individual characters to their numeric values.
        system_name: Human-readable system name used in the error message.

    Returns:
        The sum of the values of all characters in ``numeral``.

    Raises:
        ValueError: If any character is not present in ``from_map``.
    """
    return char_sum_from_numeral(numeral[::-1], from_map, system_name)


def subtractive_to_numeral(number: int, numeral_map: Mapping[int, str]) -> str:
    """Convert an integer to a numeral string using subtractive decomposition.

    Iterates the map in its defined order (largest denomination first). For each
    denomination, the corresponding glyph is appended and the denomination
    subtracted as many times as it fits, rather than using ``divmod``. This
    allows multi-character subtractive pairs (e.g. ⅠⅩ for 9) to be expressed
    as single map entries.

    Args:
        number: The Arabic number to convert.
        numeral_map: Ordered mapping from denomination values to their glyphs.
            May include subtractive pairs as multi-character glyph values.

    Returns:
        The numeral string representation of ``number``.
    """
    result = ""
    for value, glyph in numeral_map.items():
        while number >= value:
            result += glyph
            number -= value
    return result


def subtractive_from_numeral(
    numeral: str,
    from_map: Mapping[str, int],
    system_name: str,
) -> int:
    """Convert a subtractive numeral string to an integer.

    Scans ``numeral`` right-to-left (after upper-casing). A character whose
    value is smaller than the previously seen character's value is subtracted
    rather than added, implementing the standard subtractive rule
    (e.g. ⅠⅩ → 9).

    Args:
        numeral: The numeral string to convert.
        from_map: Mapping from individual characters to their numeric values.
            Both upper- and lower-case variants should be included.
        system_name: Human-readable system name used in the error message.

    Returns:
        The integer value of ``numeral``.

    Raises:
        ValueError: If any character is not present in ``from_map``.
    """
    total = 0
    prev_value = 0
    for char in reversed(numeral.upper()):
        current_value = from_map.get(char)
        if current_value is None:
            raise ValueError(f"Invalid {system_name} character: {char!r}")
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value
    return total


def longest_match_from_numeral(  # noqa: PLR0913
    numeral: str,
    from_map: Mapping[str, int],
    system_name: str,
    *,
    case_fold: bool = False,
    enforce_descending: bool = False,
    initial_max: int | None = None,
) -> int:
    """Convert a numeral string to an integer using longest-match scanning.

    At each position the longest token in ``from_map`` that matches the remaining
    string is consumed. Map entries must therefore be ordered longest-first when
    ambiguous prefixes exist (e.g. two-character thousands tokens before their
    constituent single-character units in Milesian Greek).

    Args:
        numeral: The numeral string to convert.
        from_map: Ordered mapping from token strings to their numeric values.
            Tokens are tested in iteration order; list longer tokens first.
        system_name: Human-readable system name used in error messages.
        case_fold: If ``True``, ``numeral`` is upper-cased before processing so
            that both cases are accepted without duplicating map entries.
        enforce_descending: If ``True``, token values must be non-increasing
            left-to-right. A token whose value exceeds the previous token's
            value raises ``ValueError``.
        initial_max: Sentinel used as the "previous value" before the first
            token when ``enforce_descending`` is ``True``. Defaults to
            ``max(from_map.values()) + 1``, permitting any valid first token.

    Returns:
        The integer value of ``numeral``.

    Raises:
        ValueError: If an unrecognised token is encountered, or if
            ``enforce_descending`` is ``True`` and a token violates the
            descending-order constraint.
    """
    if case_fold:
        numeral = numeral.upper()

    last_value: int = (
        (initial_max if initial_max is not None else max(from_map.values()) + 1)
        if enforce_descending
        else 0
    )

    total = 0
    i = 0
    while i < len(numeral):
        matched = False
        for symbol, value in from_map.items():
            if numeral.startswith(symbol, i):
                if enforce_descending and value > last_value:
                    raise ValueError(
                        f"Invalid {system_name} sequence: {symbol!r} cannot follow"
                        " a smaller value."
                    )
                total += value
                last_value = value
                i += len(symbol)
                matched = True
                break

        if not matched:
            raise ValueError(
                f"Invalid {system_name} character at position {i}: {numeral[i]!r}"
            )

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
