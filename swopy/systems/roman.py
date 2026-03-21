"""Roman numeral system converters.

This module implements numeral systems from the Roman script family.
Currently supports:

    Early        (Roman numerals up to 899; subtractive notation)
    Standard     (Roman numerals 1/12 to 3,999; subtractive + base-12 fractions)
    Apostrophus  (Roman numerals 1 to 100,000; extended forms CⅠↃ, CCⅠↃↃ, etc.)

All three systems use subtractive notation (e.g. ⅠⅤ for 4, ⅠⅩ for 9) for
encoding and longest-match or subtractive scanning for decoding.  Standard
additionally supports base-12 fractions (twelfths) expressed with dot and S
symbols.  Apostrophus extends the alphabet with parenthetical forms for large
values.
"""

# ruff: noqa: RUF001, RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    longest_match_from_numeral,
    subtractive_from_numeral,
    subtractive_to_numeral,
)


class Early(System[str, int]):
    """Implements bidirectional conversion between integers and Early Roman numerals.

    - Uses Unicode block U+2160-U+216E (Roman numeral characters); ASCII I, V, X,
      L, C, D are also accepted as input
    - The system is subtractive with dedicated signs for 1, 5, 10, 50, 100, and 500
      (no M; maximum is 899 = DCCCXCIX)

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (899)
        maximum_is_many: False - integers greater than 899 are not representable
        encodings: UTF-8 and ASCII
    """

    _to_numeral_map: Mapping[int, str] = {
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
    _from_numeral_map: Mapping[str, int] = {
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

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 899
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., ⅠⅤ for 4, ⅠⅩ for 9).

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

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
            ValueError: Number must be less than or equal to 899.
        """
        return subtractive_to_numeral(denotation, cls._to_numeral_map)

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
            ValueError: Invalid Early character: 'Z'
        """
        return subtractive_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Standard(System[str, int | Fraction]):
    """Implements bidirectional conversion between integers or fractions and Standard
    Roman numerals.

    - Uses Unicode block U+2160-U+216F (Roman numeral characters); ASCII I, V, X, L, C,
      D, M are also accepted as input
    - The system is subtractive for integers (e.g. ⅠⅤ for 4, ⅠⅩ for 9, ⅩⅬ for 40)
    - Base-12 fractions (1/12-11/12) are expressed with dot (·) and S notation

    Attributes:
        minimum: Minimum valid value (1/12)
        maximum: Maximum valid value (3,999)
        maximum_is_many: False - integers greater than 3,999 are not representable
        encodings: UTF-8 and ASCII
    """

    _to_numeral_map: Mapping[int | Fraction, str] = {
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
        Fraction(11, 12): "S⁙",
        Fraction(5, 6): "S∷",
        Fraction(3, 4): "S∴",
        Fraction(2, 3): "S:",
        Fraction(7, 12): "S·",
        Fraction(1, 2): "S",
        Fraction(5, 12): "⁙",
        Fraction(1, 3): "∷",
        Fraction(1, 4): "∴",
        Fraction(1, 6): ":",
        Fraction(1, 12): "·",
    }
    _from_numeral_map: Mapping[str, int | Fraction] = {
        "·": Fraction(1, 12),
        "··": Fraction(1, 6),
        ":": Fraction(1, 6),
        "···": Fraction(1, 4),
        "∴": Fraction(1, 4),
        "····": Fraction(1, 3),
        "∷": Fraction(1, 3),
        "·····": Fraction(5, 12),
        "⁙": Fraction(5, 12),
        "S": Fraction(1, 2),
        "S·": Fraction(7, 12),
        "S··": Fraction(2, 3),
        "S:": Fraction(2, 3),
        "S···": Fraction(3, 4),
        "S∴": Fraction(3, 4),
        "S····": Fraction(5, 6),
        "S∷": Fraction(5, 6),
        "S·····": Fraction(11, 12),
        "S⁙": Fraction(11, 12),
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

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 12)
    maximum: ClassVar[int | float | Fraction] = 3_999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

    @classmethod
    def _to_numeral(cls, denotation: int | Fraction) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., ⅠⅤ for 4, ⅠⅩ for 9).

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Standard.to_numeral(1)
            'Ⅰ'
            >>> Standard.to_numeral(9)
            'ⅠⅩ'
            >>> Standard.to_numeral(0)
            Traceback (most recent call last):
                ...
            ValueError: Denotation must be greater or equal to 1.
            >>> Standard.to_numeral(4000)
            Traceback (most recent call last):
                ...
            ValueError: Denotation must be less than or equal to 899.
        """
        result: str = ""

        integer = int(denotation)
        proper_fraction = denotation - integer

        for arabic, roman in cls._to_numeral_items:
            while integer >= arabic:
                result += roman
                integer -= arabic
            if not integer:
                break

        if proper_fraction == 0:
            return result

        fraction_glyph = cls._to_numeral_map.get(proper_fraction)
        if fraction_glyph is None:
            raise ValueError(f"{denotation} cannot be represented in {cls.__name__}.")

        return result + fraction_glyph

    @classmethod
    def _from_numeral(cls, numeral: str) -> int | Fraction:
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
        total: int | Fraction = 0
        prev_value: int | Fraction = 0
        prev_char: str | None = None

        for char in reversed(numeral.upper()):
            current_value = cls.from_numeral_map().get(char)

            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")

            if char == "S" and prev_char:
                combined_value = cls.from_numeral_map().get(char + prev_char)
                if combined_value is None:
                    raise ValueError(f"Invalid Roman character: {char + prev_char}")
                total += combined_value - prev_value
            elif current_value < prev_value:
                total -= current_value
            else:
                total += current_value

            prev_value = current_value
            prev_char = char

        return total


class Apostrophus(Early):
    """Implements bidirectional conversion between integers and Apostrophus Roman
    numerals.

    - Uses Unicode block U+2160-U+2169 plus multi-character Apostrophus forms (CⅠↃ,
      CCⅠↃↃ, ⅠↃↃ, ⅠↃↃↃ, CCCⅠↃↃↃ); ASCII I, V, X, L are also accepted as input
    - The system is subtractive with dedicated signs for 1, 5, 10, 50, and 100,
      extended by Apostrophus forms for 500, 1,000, 5,000, 10,000, 50,000, and 100,000
    - Longest-match decoding resolves multi-character tokens before constituent
      characters; descending order is enforced

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (100,000)
        maximum_is_many: False - integers greater than 100,000 are not representable
        encodings: UTF-8 and ASCII
    """

    _to_numeral_map: Mapping[int, str] = {
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
    _from_numeral_map: Mapping[str, int] = {
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

    maximum: ClassVar[int | float | Fraction] = 100_000
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

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
            ValueError: Invalid Roman character: Z
            >>> Apostrophus.from_numeral('VX')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Apostrophus sequence: 'X' cannot follow a smaller value.
        """
        return longest_match_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls.__name__,
            case_fold=True,
            enforce_descending=True,
            initial_max=int(cls.maximum) + 1,
        )
