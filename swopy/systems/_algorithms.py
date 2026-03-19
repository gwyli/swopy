"""Shared algorithm functions for numeral system conversions."""

# ruff: noqa: RUF002

from collections.abc import Iterable, Mapping
from fractions import Fraction
from typing import overload


def positional_to_numeral(number: int, to_map: Mapping[int, str], base: int) -> str:
    """Convert a non-negative integer to its positional base-N numeral string.

    Encodes ``number`` in base ``base``, emitting the most-significant digit
    first (left-to-right). Zero is represented by the single glyph ``to_map[0]``.

    Args:
        number: The non-negative integer to convert.
        to_map: Mapping from digit values (0 to base-1) to their glyphs.
        base: The positional base (e.g. 7, 10, 20).

    Returns:
        The numeral string representation of ``number``.
    """
    if number == 0:
        return to_map[0]
    parts: list[str] = []
    while number:
        remainder = number % base
        number //= base
        parts.append(to_map[remainder])
    return "".join(reversed(parts))


def positional_from_numeral(
    numeral: str, from_map: Mapping[str, int], system_name: str, base: int
) -> int:
    """Convert a positional base-N numeral string to its integer value.

    Scans each character left-to-right, accumulating
    ``total = total * base + digit``.

    Args:
        numeral: The numeral string to convert.
        from_map: Mapping from digit glyphs to their values (0 to base-1).
        system_name: Human-readable system name used in the error message.
        base: The positional base (e.g. 7, 10, 20).

    Returns:
        The integer value of ``numeral``.

    Raises:
        ValueError: If any character is not present in ``from_map``.
    """
    total = 0
    for char in numeral:
        if char not in from_map:
            raise ValueError(f"Invalid {system_name} character: {char!r}")
        total = total * base + from_map[char]
    return total


def greedy_additive_to_numeral(
    number: int, numeral_items: Iterable[tuple[int, str]]
) -> str:
    """Convert an integer to a numeral string using greedy additive decomposition.

    Iterates the items in their defined order (largest denomination first),
    consuming as many copies of each denomination as fit, and concatenates the
    corresponding glyphs.

    Args:
        number: The Arabic number to convert.
        numeral_items: Ordered iterable of ``(denomination, glyph)`` pairs,
            largest denomination first.  Callers should pass a pre-computed
            items tuple (e.g. ``cls._to_numeral_items``) to avoid repeated
            ``dict.items()`` view allocations on the hot path.

    Returns:
        The numeral string representation of ``number``.
    """
    result: str = ""
    for value, glyph in numeral_items:
        if value > number:
            continue
        count = number // value
        number %= value
        result += glyph * count
        if not number:
            break
    return result


def reversed_greedy_additive_to_numeral(
    number: int, numeral_items: Iterable[tuple[int, str]]
) -> str:
    """Convert an integer to a right-to-left numeral string.

    Uses greedy additive decomposition (see ``greedy_additive_to_numeral``) then
    reverses the result so that the highest-denomination glyph appears rightmost,
    matching writing systems that read right-to-left (e.g. Etruscan).

    Args:
        number: The Arabic number to convert.
        numeral_items: Ordered iterable of ``(denomination, glyph)`` pairs,
            largest denomination first.  See ``greedy_additive_to_numeral``.

    Returns:
        The numeral string representation of ``number``, with glyphs in
        right-to-left order (largest denomination rightmost).
    """
    return greedy_additive_to_numeral(number, numeral_items)[::-1]


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
        if not number:
            break
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
            if numeral[i] == symbol[0] and numeral.startswith(symbol, i):
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
    thousands = number // 1000
    number = number % 1000
    if thousands:
        if thousands > 1:
            result += numeral_map[thousands]
        result += numeral_map[1000]

    # Hundreds group: unit multiplier (omitted if 1) + hundreds glyph
    hundreds = number // 100
    number = number % 100
    if hundreds:
        if hundreds > 1:
            result += numeral_map[hundreds]
        result += numeral_map[100]

    # Tens: dedicated decade glyph
    tens = number // 10
    number = number % 10
    if tens:
        result += numeral_map[tens * 10]

    # Ones: dedicated unit glyph
    if number:
        result += numeral_map[number]

    return result


def multiplicative_myriad_to_numeral(
    number: int,
    digit_map: Mapping[int, str],
    multiplier_map: Mapping[int, str],
    *,
    explicit_one_tens: bool = False,
) -> str:
    """Convert an integer to a multiplicative-myriad numeral string.

    Handles systems (e.g. Tangut, Khitan) where digits 1–9 have unique glyphs
    and multipliers x10, x100, x1000, x10,000 are separate glyphs. The
    coefficient is omitted when equal to 1, except optionally for the tens
    place. The myriad coefficient (1–9999) is itself encoded as a sub-myriad
    number.

    Args:
        number: The Arabic number to convert.
        digit_map: Ordered mapping from digit values (1–9) to their glyphs.
        multiplier_map: Ordered mapping from multiplier values (10000, 1000,
            100, 10) to their glyphs, largest first.
        explicit_one_tens: If ``True``, the digit 1 is always written before
            the tens multiplier (e.g. Tangut). If ``False``, the digit 1 is
            omitted before all multipliers including tens (e.g. Khitan).

    Returns:
        The numeral string representation of ``number``.
    """
    _myriad = 10000
    _ten = 10
    myriad_glyph = multiplier_map[_myriad]
    sub_mult = [(k, v) for k, v in multiplier_map.items() if k != _myriad]

    def encode_sub(n: int) -> str:
        res = ""
        for mult, glyph in sub_mult:
            coeff = n // mult
            n = n % mult
            if coeff:
                if coeff > 1 or (explicit_one_tens and mult == _ten):
                    res += digit_map[coeff]
                res += glyph
        if n:
            res += digit_map[n]
        return res

    myriads = number // _myriad
    remainder = number % _myriad
    result = ""
    if myriads:
        if myriads > 1 or explicit_one_tens:
            result += encode_sub(myriads)
        result += myriad_glyph
    if remainder:
        result += encode_sub(remainder)
    return result


def multiplicative_myriad_from_numeral(
    numeral: str,
    digit_map: Mapping[str, int],
    multiplier_map: Mapping[str, int],
    system_name: str,
) -> int:
    """Convert a multiplicative-myriad numeral string to an integer.

    Splits at the myriad glyph (if present). The portion before is parsed as
    a sub-myriad coefficient (multiplied by 10,000); the portion after is
    parsed as the remainder. If no myriad glyph is present, the whole string
    is parsed as a sub-myriad number.

    Within each sub-myriad segment, a digit glyph followed by a sub-myriad
    multiplier glyph contributes ``digit × multiplier``; a lone multiplier
    glyph contributes ``1 × multiplier``; a lone digit glyph contributes its
    value.

    Args:
        numeral: The numeral string to convert.
        digit_map: Mapping from digit glyphs to their values (1–9).
        multiplier_map: Mapping from multiplier glyphs to their values
            (10000, 1000, 100, 10).
        system_name: Human-readable system name used in the error message.

    Returns:
        The integer value of ``numeral``.

    Raises:
        ValueError: If an unrecognised character is encountered.
    """
    items = list(multiplier_map.items())
    myriad_glyph = items[0][0]
    sub_mult_map = dict(items[1:])

    def parse_sub(s: str) -> int:
        total = 0
        i = 0
        while i < len(s):
            c = s[i]
            if c in digit_map:
                digit = digit_map[c]
                i += 1
                if i < len(s) and s[i] in sub_mult_map:
                    total += digit * sub_mult_map[s[i]]
                    i += 1
                else:
                    total += digit
            elif c in sub_mult_map:
                total += sub_mult_map[c]
                i += 1
            else:
                raise ValueError(f"Invalid {system_name} character: {c!r}")
        return total

    if myriad_glyph in numeral:
        idx = numeral.index(myriad_glyph)
        coeff = parse_sub(numeral[:idx]) if idx > 0 else 1
        remainder = parse_sub(numeral[idx + 1 :]) if idx + 1 < len(numeral) else 0
        return coeff * 10000 + remainder
    return parse_sub(numeral)


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
    total = 0
    unit_buffer = 0

    for char in numeral:
        v = from_map.get(char)
        if v is None:
            raise ValueError(f"Invalid {system_name} character: {char!r}")

        if 1 <= v <= 9:  # noqa: PLR2004
            unit_buffer += v
        elif v in {100, 1000}:
            total += v * max(unit_buffer, 1)
            unit_buffer = 0
        else:
            # Decade glyph: flush accumulated units as ones first
            total += unit_buffer
            unit_buffer = 0
            total += v

    total += unit_buffer
    return total
