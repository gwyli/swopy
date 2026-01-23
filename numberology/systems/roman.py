"""Roman numeral system conversion module.

This module provides conversion utilities for Roman numerals (I, V, X, L, C, D, M).
It implements bidirectional conversion between integers (1-3999) and Roman numeral
string representations, with support for subtractive notation (e.g., IV for 4, IX for 9)
"""

FROM_INT: list[tuple[int, str]] = [
    (1_000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]
TO_INT: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1_000,
}

MINIMUM: int = 1
MAXIMUM: int = 3_999

MAXIMUM_IS_MANY: bool = False


def _limits(number: int) -> int:
    """Validates that a number is within acceptable limits for Roman numerals.

    Checks if the given number falls within the valid range for Roman numeral
    representation (1 to 3999).

    Args:
        number: The number to validate.

    Returns:
        The validated number.

    Raises:
        ValueError: If the number is not in the range 1..3999.

    Examples:
        >>> _limits(1)
        1
        >>> _limits(3999)
        3999
        >>> _limits(0)
        Traceback (most recent call last):
            ...
        ValueError: Number must be between 1 and 3999
        >>> _limits(4000)
        Traceback (most recent call last):
            ...
        ValueError: Number must be between 1 and 3999
    """

    if not (MINIMUM <= number <= MAXIMUM):
        raise ValueError("Number must be between 1 and 3999")
    return number


def from_int(number: int) -> str:
    """Converts an integer to a Roman numeral string.

    Takes an integer and converts it to its Roman numeral representation,
    using subtractive notation where appropriate (e.g., IV for 4, IX for 9).

    Args:
        number: The integer to convert, must be between 1 and 3999.

    Returns:
        The Roman numeral string representation of the number.

    Raises:
        ValueError: If the number is outside the valid range.

    Examples:
        >>> from_int(1)
        'I'
        >>> from_int(10)
        'X'
        >>> from_int(4)
        'IV'
        >>> from_int(9)
        'IX'
        >>> from_int(42)
        'XLII'
        >>> from_int(1994)
        'MCMXCIV'
    """
    result: str = ""
    number_ = _limits(number)

    for latin, roman in FROM_INT:
        while number_ >= latin:
            result += roman
            number_ -= latin

    return result


def to_int(number: str) -> int:
    """Converts a Roman numeral to an integer.

    Takes a Roman numeral and converts it to its integer equivalent,
    properly handling subtractive notation (e.g., IV -> 4, IX -> 9).

    Args:
        number: The Roman numeral to convert.

    Returns:
        The integer representation of the Roman numeral.

    Raises:
        ValueError: If the string contains invalid Roman numerals.

    Examples:
        >>> to_int('I')
        1
        >>> to_int('X')
        10
        >>> to_int('IV')
        4
        >>> to_int('IX')
        9
        >>> to_int('XLII')
        42
        >>> to_int('MCMXCIV')
        1994
        >>> to_int('i')  # Case insensitive
        1
        >>> to_int('Z')
        Traceback (most recent call last):
            ...
        ValueError: Invalid Roman character: Z
    """
    total: int = 0
    prev_value: int = 0
    for char in reversed(number.upper()):
        current_value = TO_INT.get(char)
        if current_value is None:
            raise ValueError(f"Invalid Roman character: {char}")
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value

    return _limits(total)
