"""Latin numeral system conversion module.

This module provides conversion utilities for Latin numerals. Latin numerals
use ↀ (vinculum representing 1000) in place of M, and use the same characters
(I, V, X, L, C, D) for other values and support subtractive notation (e.g., IV for 4,
IX for 9).
"""

from typing import ClassVar

from numberology.system import System


class Latin(System[str]):
    """Latin numeral system converter.

    Implements bidirectional conversion between integers and Latin numeral strings.
    Latin numerals use ↀ (vinculum representing 1000) instead of M, and support
    subtractive notation (e.g., IV for 4, IX for 9).

    Type Parameter:
        str: Latin numerals are represented as strings (I, V, X, L, C, D, ↀ, etc.).

    Attributes:
        from_int_: Mapping of integer values to Latin numeral components,
                   ordered by magnitude including subtractive pairs.
        to_int_: Mapping of Latin numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (3999), limited by Latin numeral notation.
        maximum_is_many: False, as 3999 is a precise limit.
    """

    from_int_: ClassVar[dict[int, str]] = {
        1_000: "ↀ",
        900: "Cↀ",
        500: "D",
        400: "CD",
        100: "C",
        90: "XC",
        50: "L",
        40: "XL",
        10: "X",
        9: "IX",
        5: "V",
        4: "IV",
        1: "I",
    }
    to_int_: ClassVar[dict[str, int]] = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "ↀ": 1_000,
    }

    minimum: ClassVar[int] = 1
    maximum: ClassVar[int] = 3_999

    maximum_is_many: ClassVar[bool] = False

    @classmethod
    def from_int(cls, number: int) -> str:
        """Converts an integer to a Latin numeral string.

        Takes an integer and converts it to its Latin numeral representation,
        using subtractive notation where appropriate (e.g., IV for 4, IX for 9).

        Args:
            number: The integer to convert.

        Returns:
            The Latin numeral representation of the number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Latin.from_int(1)
            'I'
            >>> Latin.from_int(9)
            'IX'
            >>> Latin.from_int(1994)
            'ↀCↀXCIV'
            >>> Latin.from_int(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be greater or equal to 1.
            >>> Latin.from_int(4000)
            Traceback (most recent call last):
                ...
            ValueError: Number must be less than or equal to 3999.
        """
        result: str = ""
        number_ = cls._limits(number)

        for value, latin in cls.from_int_.items():
            while number_ >= value:
                result += latin
                number_ -= value

        return result

    @classmethod
    def to_int(cls, number: str) -> int:
        """Converts a Latin numeral to an integer.

        Takes a Latin numeral and converts it to its integer equivalent,
        properly handling subtractive notation (e.g., IV -> 4, IX -> 9).

        Args:
            number: The Latin numeral to convert.

        Returns:
            The integer representation of the Latin numeral.

        Raises:
            ValueError: If the string contains invalid Latin numerals.

        Examples:
            >>> Latin.to_int('X')
            10
            >>> Latin.to_int('IX')
            9
            >>> Latin.to_int('ↀCↀXCIV')
            1994
            >>> Latin.to_int('i')  # Case insensitive
            1
            >>> Latin.to_int('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Latin character: Z
        """
        total: int = 0
        prev_value: int = 0

        for char in reversed(number.upper()):
            current_value = cls.to_int_.get(char)

            if current_value is None:
                raise ValueError(f"Invalid Latin character: {char}")

            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value

        return cls._limits(total)
