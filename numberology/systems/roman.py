"""Roman numeral system conversion module.

This module provides conversion utilities for Roman numerals (I, V, X, L, C, D, M).
It implements bidirectional conversion between integers (1-3999) and Roman numeral
string representations, with support for subtractive notation (e.g., IV for 4, IX for
9).
"""

from typing import ClassVar

from numberology.system import System


class Early(System[str, int]):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., IV for 4, IX for 9, XL for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (I, V, X, L, C, D, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (899), limited by Roman numeral notation.
        maximum_is_many: False, as 899 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
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
    from_numeral_map: ClassVar[dict[str, int]] = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
    }

    minimum: ClassVar[float] = 1
    maximum: ClassVar[float] = 899

    maximum_is_many: ClassVar[bool] = False

    @classmethod
    def to_numeral(cls, number: int) -> str:
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
            >>> Early.to_numeral(1)
            'I'
            >>> Early.to_numeral(9)
            'IX'
            >>> Early.to_numeral(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be greater or equal to 1.
            >>> Early.to_numeral(900)
            Traceback (most recent call last):
                ...
            ValueError: Number must be less than or equal to 900.
        """
        result: str = ""
        number_ = cls._limits(number)

        for latin, roman in cls.to_numeral_map.items():
            while number_ >= latin:
                result += roman
                number_ -= latin

        return result

    @classmethod
    def from_numeral(cls, number: str) -> int:
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
            >>> Early.from_numeral('X')
            10
            >>> Early.from_numeral('IX')
            9
            >>> Early.from_numeral('i')  # Case insensitive
            1
            >>> Early.from_numeral('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Roman character: Z
        """
        total: int = 0
        prev_value: int = 0

        for char in reversed(number.upper()):
            current_value = cls.from_numeral_map.get(char)

            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")

            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value

        return cls._limits(total)


# FIXME: Add fractions
class Standard(Early):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., IV for 4, IX for 9, XL for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (I, V, X, L, C, D, M, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (3999), limited by Roman numeral notation.
        maximum_is_many: False, as 3999 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
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
    from_numeral_map: ClassVar[dict[str, int]] = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1_000,
    }

    maximum: ClassVar[float] = 3_999


class Apostrophus(Early):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., IV for 4, IX for 9, XL for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (I, V, X, L, C, D, CIↃ, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (3999), limited by Roman numeral notation.
        maximum_is_many: False, as 3999 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
        100_000: "CCCIↃↃↃ",
        50_000: "IↃↃↃ",
        10_000: "CCIↃↃ",
        5_000: "IↃↃ",
        1_000: "CIↃ",
        500: "IↃ",
        100: "C",
        50: "L",
        10: "X",
        5: "V",
        1: "I",
    }
    from_numeral_map: ClassVar[dict[str, int]] = {
        "CCCIↃↃↃ": 100_000,
        "IↃↃↃ": 50_000,
        "CCIↃↃ": 10_000,
        "IↃↃ": 5_000,
        "CIↃ": 1_000,
        "IↃ": 500,
        "C": 100,
        "L": 50,
        "X": 10,
        "V": 5,
        "I": 1,
    }

    maximum: ClassVar[float] = 100_000

    @classmethod
    def from_numeral(cls, number: str) -> int:
        """
        #FIXME: Add docstring
        """
        total = 0

        i = 0
        while i < len(number):
            matched = False
            # Check for multi-character symbols first (greedy match)
            for symbol, value in cls.from_numeral_map.items():
                if number.startswith(symbol, i):
                    total += value
                    i += len(symbol)
                    matched = True
                    break

            if not matched:
                raise ValueError(f"Invalid Apostrophus characters at position {i}")

        return cls._limits(total)
