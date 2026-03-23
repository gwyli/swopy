"""Arabic numeral system converters.

This module implements numeral systems from the Arabic script family.
Currently supports:

    Rumi  U+10E60-U+10E7E  (Rumi Numeral Symbols block)

Rumi is a purely additive system written right-to-left (largest denomination
on the right).  Integers use greedy decomposition followed by reversal;
fractions (1/4, 1/3, 1/2, 2/3) are appended after the reversed integer string.

The Arabic class is re-exported from hindu_arabic for backward compatibility.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)
from .hindu_arabic import Arabic

__all__ = ["Arabic", "Rumi"]


class Rumi(System[str, int | Fraction]):
    """Implements bidirectional conversion between integers or fractions and
    Rumi numerals.

    - Uses Unicode block U+10E60-U+10E7E (27 glyphs: 1-9, 10-90, 100-900,
      and four fraction signs for 1/2, 1/4, 1/3, and 2/3)
    - The system is purely additive and written right-to-left (largest denomination
      on the right)
    - Fractions are appended to the reversed integer string

    Attributes:
        minimum: Minimum valid value (1/4)
        maximum: Maximum valid value (999)
        maximum_is_many: False - integers greater than 999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 4)
    maximum: ClassVar[int | float | Fraction] = 999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int | Fraction, str] = {
        900: "\U00010e7a",  # 𐹺 RUMI NUMBER NINE HUNDRED
        800: "\U00010e79",  # 𐹹 RUMI NUMBER EIGHT HUNDRED
        700: "\U00010e78",  # 𐹸 RUMI NUMBER SEVEN HUNDRED
        600: "\U00010e77",  # 𐹷 RUMI NUMBER SIX HUNDRED
        500: "\U00010e76",  # 𐹶 RUMI NUMBER FIVE HUNDRED
        400: "\U00010e75",  # 𐹵 RUMI NUMBER FOUR HUNDRED
        300: "\U00010e74",  # 𐹴 RUMI NUMBER THREE HUNDRED
        200: "\U00010e73",  # 𐹳 RUMI NUMBER TWO HUNDRED
        100: "\U00010e72",  # 𐹲 RUMI NUMBER ONE HUNDRED
        90: "\U00010e71",  # 𐹱 RUMI NUMBER NINETY
        80: "\U00010e70",  # 𐹰 RUMI NUMBER EIGHTY
        70: "\U00010e6f",  # 𐹯 RUMI NUMBER SEVENTY
        60: "\U00010e6e",  # 𐹮 RUMI NUMBER SIXTY
        50: "\U00010e6d",  # 𐹭 RUMI NUMBER FIFTY
        40: "\U00010e6c",  # 𐹬 RUMI NUMBER FORTY
        30: "\U00010e6b",  # 𐹫 RUMI NUMBER THIRTY
        20: "\U00010e6a",  # 𐹪 RUMI NUMBER TWENTY
        10: "\U00010e69",  # 𐹩 RUMI NUMBER TEN
        9: "\U00010e68",  # 𐹨 RUMI NUMBER NINE
        8: "\U00010e67",  # 𐹧 RUMI NUMBER EIGHT
        7: "\U00010e66",  # 𐹦 RUMI NUMBER SEVEN
        6: "\U00010e65",  # 𐹥 RUMI NUMBER SIX
        5: "\U00010e64",  # 𐹤 RUMI NUMBER FIVE
        4: "\U00010e63",  # 𐹣 RUMI NUMBER FOUR
        3: "\U00010e62",  # 𐹢 RUMI NUMBER THREE
        2: "\U00010e61",  # 𐹡 RUMI NUMBER TWO
        1: "\U00010e60",  # 𐹠 RUMI NUMBER ONE
        Fraction(2, 3): "\U00010e7e",  # 𐹾 RUMI FRACTION TWO THIRDS
        Fraction(1, 2): "\U00010e7b",  # 𐹻 RUMI FRACTION ONE HALF
        Fraction(1, 3): "\U00010e7d",  # 𐹽 RUMI FRACTION ONE THIRD
        Fraction(1, 4): "\U00010e7c",  # 𐹼 RUMI FRACTION ONE QUARTER
    }

    _from_numeral_map: Mapping[str, int | Fraction] = {
        v: k for k, v in _to_numeral_map.items()
    }

    @classmethod
    def _to_numeral(cls, denotation: int | Fraction) -> str:
        """Convert an integer or fraction to Rumi numerals.

        The integer part uses greedy additive decomposition, largest denomination
        first, then reversed for right-to-left ordering.  The fractional part (if
        any) is looked up directly in the map and appended.

        Examples:
            >>> Rumi._to_numeral(1)
            '𐹠'
            >>> Rumi._to_numeral(9)
            '𐹨'
            >>> Rumi._to_numeral(10)
            '𐹩'
            >>> Rumi._to_numeral(11)
            '𐹠𐹩'
            >>> Rumi._to_numeral(999)
            '𐹨𐹱𐹺'
            >>> from fractions import Fraction
            >>> Rumi._to_numeral(Fraction(1, 2))
            '𐹻'
            >>> Rumi._to_numeral(Fraction(3, 2))
            '𐹠𐹻'
            >>> Rumi._to_numeral(Fraction(5, 6))
            Traceback (most recent call last):
                ...
            ValueError: 5/6 cannot be represented in Rumi.
        """
        if isinstance(denotation, int):
            return reversed_greedy_additive_to_numeral(
                denotation, cls._to_numeral_items
            )

        frac = Fraction(denotation)
        integer_part = int(frac)
        frac_part = frac - integer_part

        result = (
            reversed_greedy_additive_to_numeral(integer_part, cls._to_numeral_items)
            if integer_part
            else ""
        )

        if frac_part:
            frac_glyph = cls._to_numeral_map.get(frac_part)
            if frac_glyph is None:
                raise ValueError(
                    f"{denotation} cannot be represented in {cls.__name__}."
                )
            result += frac_glyph

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int | Fraction:
        """Convert a Rumi numeral to an integer or fraction.

        Sums the values of each glyph in the string.

        Examples:
            >>> Rumi._from_numeral('𐹠')
            1
            >>> Rumi._from_numeral('𐹨')
            9
            >>> Rumi._from_numeral('𐹩')
            10
            >>> Rumi._from_numeral('𐹠𐹩')
            11
            >>> Rumi._from_numeral('𐹨𐹱𐹺')
            999
            >>> Rumi._from_numeral('𐹻')
            Fraction(1, 2)
            >>> Rumi._from_numeral('𐹠𐹻')
            Fraction(3, 2)
            >>> Rumi._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Rumi character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
