"""Cuneiform numeral system converters.

This module implements numeral systems from the Cuneiform script family.
Currently supports:

    Cuneiform  U+12400-U+1247F  (Cuneiform Numbers and Punctuation block)
               U+12000-U+123FF  (main block; ASH and DISH base signs)

Cuneiform is a purely additive system using greedy decomposition for encoding
and character-sum for decoding.  Multiple-of-10 signs (THREE DISH through
NINE DISH) and unit signs (TWO ASH through NINE ASH) are combined greedily;
the value 20 is represented by two DISH signs.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Cuneiform(System[str, int]):
    """Implements bidirectional conversion between integers and Cuneiform numerals.

    - Uses Unicode blocks U+12400-U+1247F (Numbers and Punctuation) and
      U+12000-U+123FF (main block)
    - The system is purely additive, with pre-composed signs for units
      (TWO ASH-NINE ASH) and multiples of 10 (THREE DISH-NINE DISH)
    - Value 20 is represented by two DISH signs; the base ASH (1) and DISH (10)
      come from the main block

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (999)
        maximum_is_many: False - integers greater than 999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        90: "\U0001240e",  # 𒐎 CUNEIFORM NUMERIC SIGN NINE DISH
        80: "\U0001240d",  # 𒐍 CUNEIFORM NUMERIC SIGN EIGHT DISH
        70: "\U0001240c",  # 𒐌 CUNEIFORM NUMERIC SIGN SEVEN DISH
        60: "\U0001240b",  # 𒐋 CUNEIFORM NUMERIC SIGN SIX DISH
        50: "\U0001240a",  # 𒐊 CUNEIFORM NUMERIC SIGN FIVE DISH
        40: "\U00012409",  # 𒐉 CUNEIFORM NUMERIC SIGN FOUR DISH
        30: "\U00012408",  # 𒐈 CUNEIFORM NUMERIC SIGN THREE DISH
        10: "\U00012079",  # 𒁹 CUNEIFORM SIGN DISH (ONE DISH = 10)
        9: "\U00012407",  # 𒐇 CUNEIFORM NUMERIC SIGN NINE ASH
        8: "\U00012406",  # 𒐆 CUNEIFORM NUMERIC SIGN EIGHT ASH
        7: "\U00012405",  # 𒐅 CUNEIFORM NUMERIC SIGN SEVEN ASH
        6: "\U00012404",  # 𒐄 CUNEIFORM NUMERIC SIGN SIX ASH
        5: "\U00012403",  # 𒐃 CUNEIFORM NUMERIC SIGN FIVE ASH
        4: "\U00012402",  # 𒐂 CUNEIFORM NUMERIC SIGN FOUR ASH
        3: "\U00012401",  # 𒐁 CUNEIFORM NUMERIC SIGN THREE ASH
        2: "\U00012400",  # 𒐀 CUNEIFORM NUMERIC SIGN TWO ASH
        1: "\U00012038",  # 𒀸 CUNEIFORM SIGN ASH (ONE ASH = 1)
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Cuneiform numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Cuneiform._to_numeral(1)
            '𒀸'
            >>> Cuneiform._to_numeral(9)
            '𒐇'
            >>> Cuneiform._to_numeral(10)
            '𒁹'
            >>> Cuneiform._to_numeral(15)
            '𒁹𒐃'
            >>> Cuneiform._to_numeral(31)
            '𒐈𒀸'
            >>> Cuneiform._to_numeral(99)
            '𒐎𒐇'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Cuneiform numeral string to its Arabic integer value.

        Sums the values of each glyph in the string.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Cuneiform._from_numeral('𒀸')
            1
            >>> Cuneiform._from_numeral('𒁹𒐃')
            15
            >>> Cuneiform._from_numeral('𒐈𒀸')
            31
            >>> Cuneiform._from_numeral('𒐎𒐇')
            99
            >>> Cuneiform._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Cuneiform character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
