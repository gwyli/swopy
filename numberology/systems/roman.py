"""Roman numeral system conversion module.

This module provides conversion utilities for Roman numerals (I, V, X, L, C, D, M).
It implements bidirectional conversion between integers (1-3999) and Roman numeral
string representations, with support for subtractive notation (e.g., IV for 4, IX for
9).
"""

from typing import ClassVar

from numberology.system import System


class Roman(System[str]):
    from_int_: ClassVar[dict[int, str]] = {
        1_000: "M",
        900: "CM",
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
        "M": 1_000,
    }

    minimum: ClassVar[int] = 1
    maximum: ClassVar[int] = 3_999

    maximum_is_many: ClassVar[bool] = False

    @classmethod
    def _limits(cls, number: int) -> int:
        """Validates that a number is within acceptable limits for Roman numerals.

        Checks if the given number falls within the valid range for Roman numeral
        representation.

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Roman._limits(1)
            1
            >>> Roman._limits(3999)
            3999
            >>> Roman._limits(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be between 1 and 3999
            >>> Roman._limits(4000)
            Traceback (most recent call last):
                ...
            ValueError: Number must be between 1 and 3999
        """

        if not (cls.minimum <= number <= cls.maximum):
            raise ValueError(f"Number must be between {cls.minimum} and {cls.maximum}")
        return number

    @classmethod
    def from_int(cls, number: int) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., IV for 4, IX for 9).

        Args:
            number: The integer to convert

        Returns:
            The Roman numeral representation of the number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Roman.from_int(1)
            'I'
            >>> Roman.from_int(9)
            'IX'
            >>> Roman.from_int(1994)
            'MCMXCIV'
        """
        result: str = ""
        number_ = cls._limits(number)

        for latin, roman in cls.from_int_.items():
            while number_ >= latin:
                result += roman
                number_ -= latin

        return result

    @classmethod
    def to_int(cls, number: str) -> int:
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
            >>> Roman.to_int('X')
            10
            >>> Roman.to_int('IX')
            9
            >>> Roman.to_int('MCMXCIV')
            1994
            >>> Roman.to_int('i')  # Case insensitive
            1
            >>> Roman.to_int('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Roman character: Z
        """
        total: int = 0
        prev_value: int = 0

        for char in reversed(number.upper()):
            current_value = cls.to_int_.get(char)

            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")

            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value

        return cls._limits(total)
