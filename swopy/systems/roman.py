"""Roman numeral system conversion module.

This module provides conversion utilities for Roman numerals. It implements
bidirectional conversion between Arabic numbers and Roman numerals, with support
for subtractive notation (e.g., ⅠⅤ for 4, ⅠⅩ for 9).
"""
# Ignore ambiguous unicode character strings in Roman numerals (e.g., 'I' vs 'Ⅰ').
# ruff: noqa: RUF001 RUF002 RUF003

from typing import ClassVar, Literal

from swopy.system import System


class Early[TNumeral: str, TDenotation: int](System[str, int]):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., ⅠⅤ for 4, ⅠⅩ for 9, ⅩⅬ for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (Ⅰ, Ⅴ, Ⅹ, Ⅼ, Ⅽ, Ⅾ, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (899), limited by Roman numeral notation.
        maximum_is_many: False, as 899 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
        500: "\u216e",
        400: "\u216d\u216e",
        100: "\u216d",
        90: "\u2169\u216d",
        50: "\u216c",
        40: "\u2169\u216c",
        10: "\u2169",
        9: "\u2160\u2169",
        5: "\u2164",
        4: "\u2160\u2164",
        1: "\u2160",
    }
    from_numeral_map: ClassVar[dict[str, int]] = {
        "\u2160": 1,
        "I": 1,
        "\u2164": 5,
        "V": 5,
        "\u2169": 10,
        "X": 10,
        "\u216c": 50,
        "L": 50,
        "\u216d": 100,
        "C": 100,
        "\u216e": 500,
        "D": 500,
    }

    minimum: ClassVar[float] = 1
    maximum: ClassVar[float] = 899

    maximum_is_many: ClassVar[bool] = False

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., ⅠⅤ for 4, ⅠⅩ for 9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Early.to_numeral(1)
            'Ⅰ'
            >>> Early.to_numeral(9)
            'ⅠⅩ'
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

        for latin, roman in cls.to_numeral_map.items():
            while number >= latin:
                result += roman
                number -= latin

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Converts a Roman numeral to an integer.

        Takes a Roman numeral and converts it to its integer equivalent,
        properly handling subtractive notation (e.g., ⅠⅤ -> 4, ⅠⅩ -> 9).

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Early.from_numeral('Ⅹ')
            10
            >>> Early.from_numeral('ⅠⅩ')
            9
            >>> Early.from_numeral('ⅰ')  # Case insensitive
            1
            >>> Early.from_numeral('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Roman character: Z
        """

        total: int = 0
        prev_value: int = 0

        for char in reversed(numeral.upper()):
            current_value = cls.from_numeral_map.get(char)

            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")

            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value

        return total


# FIXME: Add fractions
class Standard[TNumeral: str, TDenotation: (int)](System[str, int]):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., ⅠⅤ for 4, ⅠⅩ for 9, ⅩⅬ for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (Ⅰ, Ⅴ, Ⅹ, Ⅼ, Ⅽ, Ⅾ, Ⅿ, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (3999), limited by Roman numeral notation.
        maximum_is_many: False, as 3999 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
        1_000: "\u216f",
        900: "\u216d\u216f",
        500: "\u216e",
        400: "\u216d\u216e",
        100: "\u216d",
        90: "\u2169\u216d",
        50: "\u216c",
        40: "\u2169\u216c",
        10: "\u2169",
        9: "\u2160\u2169",
        5: "\u2164",
        4: "\u2160\u2164",
        1: "\u2160",
    }
    from_numeral_map: ClassVar[dict[str, int]] = {
        "\u2160": 1,
        "I": 1,
        "\u2164": 5,
        "V": 5,
        "\u2169": 10,
        "X": 10,
        "\u216c": 50,
        "L": 50,
        "\u216d": 100,
        "C": 100,
        "\u216e": 500,
        "D": 500,
        "\u216f": 1_000,
        "M": 1_000,
    }

    minimum: ClassVar[float] = 1
    maximum: ClassVar[float] = 3_999

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., ⅠⅤ for 4, ⅠⅩ for 9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Standard.to_numeral(1)
            'Ⅰ'
            >>> Standard.to_numeral(9)
            'ⅠⅩ'
            >>> Standard.to_numeral(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be greater or equal to 1.
            >>> Standard.to_numeral(4000)
            Traceback (most recent call last):
                ...
            ValueError: Number must be less than or equal to 900.
        """
        result: str = ""

        for latin, roman in cls.to_numeral_map.items():
            while number >= latin:
                result += roman
                number -= latin

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Converts a Roman numeral to an integer.

        Takes a Roman numeral and converts it to its integer equivalent,
        properly handling subtractive notation (e.g., ⅠⅤ -> 4, ⅠⅩ -> 9).

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Standard.from_numeral('Ⅹ')
            10
            >>> Standard.from_numeral('ⅠⅩ')
            9
            >>> Standard.from_numeral('ⅰ')  # Case insensitive
            1
            >>> Standard.from_numeral('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Roman character: Z
        """
        total: int = 0
        prev_value: int = 0

        for char in reversed(numeral.upper()):
            current_value = cls.from_numeral_map.get(char)

            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")

            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value

        return total


class Apostrophus[TNumeral: str, TDenotation: int](Early[str, int]):
    """Roman numeral system converter.

    Implements bidirectional conversion between integers and Roman numeral strings.
    Supports the standard Roman numeral notation with subtractive notation for
    efficiency (e.g., ⅠⅤ for 4, ⅠⅩ for 9, ⅩⅬ for 40).

    Type Parameter:
        str: Roman numerals are represented as strings (Ⅰ, Ⅴ, Ⅹ, Ⅼ, C, Ⅾ, CⅠↃ, etc.).

    Attributes:
        to_numeral_map: Mapping of integer values to Roman numeral components,
                   ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Roman numeral characters to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (3999), limited by Roman numeral notation.
        maximum_is_many: False, as 3999 is a precise limit.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
        100_000: "CCCⅠↃↃↃ",
        50_000: "ⅠↃↃↃ",
        10_000: "CCⅠↃↃ",
        5_000: "ⅠↃↃ",
        1_000: "CⅠↃ",
        500: "ⅠↃ",
        100: "C",
        50: "\u216c",
        10: "\u2169",
        5: "\u2164",
        1: "\u2160",
    }
    from_numeral_map: ClassVar[dict[str, int]] = {
        "CCCⅠↃↃↃ": 100_000,
        "ⅠↃↃↃ": 50_000,
        "CCⅠↃↃ": 10_000,
        "ⅠↃↃ": 5_000,
        "CⅠↃ": 1_000,
        "ⅠↃ": 500,
        "C": 100,
        "\u216c": 50,
        "L": 50,
        "\u2169": 10,
        "X": 10,
        "\u2164": 5,
        "V": 5,
        "\u2160": 1,
        "I": 1,
    }

    maximum: ClassVar[float] = 100_000
    encodings: ClassVar[set[Literal["utf8", "ascii"]]] = {"utf8"}

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Converts a Roman numeral of the Apostrophus form to an integer.

        Takes a Roman numeral and converts it to its integer equivalent,
        properly handling subtractive notation (e.g., ⅠⅤ -> 4, ⅠⅩ -> 9).

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Apostrophus.from_numeral('Ⅹ')
            10
            >>> Apostrophus.from_numeral('ⅠↃⅠ')
            501
            >>> Apostrophus.from_numeral('ⅰ')  # Case insensitive
            1
            >>> Apostrophus.from_numeral('Z')
            Traceback (most recent call last):
                ...
            ValueError: Ⅰnvalid Roman character: Z
            >>> Apostrophus.from_numeral('ⅠⅠↃⅠ')
            Traceback (most recent call last):
                ...
            ValueError: Invalid sequence I cannot follow a smaller value.
        """
        total = 0
        numeral_ = numeral.upper()
        # Start with a value larger than the maximum to allow any numeral
        last_value = cls.maximum + 1

        i = 0
        while i < len(numeral_):
            matched = False
            for symbol in cls.from_numeral_map:
                if numeral_.startswith(symbol, i):
                    current_value = cls.from_numeral_map[symbol]

                    # Ensure we aren't seeing a larger symbol after a smaller one
                    if current_value > last_value:
                        raise ValueError(
                            f"Invalid sequence {symbol} cannot follow a smaller value."
                        )

                    total += current_value
                    last_value = current_value
                    i += len(symbol)
                    matched = True
                    break

            if not matched:
                raise ValueError(f"Invalid Apostrophus characters at position {i}")

        return total
