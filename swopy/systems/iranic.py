"""Iranic numeral system converters.

This module implements numeral systems from the Iranic script family.
Currently supports:

    Chorasmian  U+10FB0-U+10FBF

Chorasmian is a purely additive system written right-to-left (largest
denomination on the right).  Encoding uses greedy decomposition followed by
reversal; decoding reverses the input before summing.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class Chorasmian(System[str, int]):
    """Implements bidirectional conversion between integers and Chorasmian numerals.

    - Uses Unicode block U+10FB0-U+10FBF (seven glyphs: 1, 2, 3, 4, 10, 20, 100)
    - The system is purely additive and written right-to-left (largest denomination
      on the right)

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (9999)
        maximum_is_many: False - integers greater than 9999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010fcb",  # 𐿋 CHORASMIAN NUMBER ONE HUNDRED
        20: "\U00010fca",  # 𐿊 CHORASMIAN NUMBER TWENTY
        10: "\U00010fc9",  # 𐿉 CHORASMIAN NUMBER TEN
        4: "\U00010fc8",  # 𐿈 CHORASMIAN NUMBER FOUR
        3: "\U00010fc7",  # 𐿇 CHORASMIAN NUMBER THREE
        2: "\U00010fc6",  # 𐿆 CHORASMIAN NUMBER TWO
        1: "\U00010fc5",  # 𐿅 CHORASMIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Chorasmian numerals.

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> Chorasmian._to_numeral(1)
            '𐿅'
            >>> Chorasmian._to_numeral(4)
            '𐿈'
            >>> Chorasmian._to_numeral(5)
            '𐿅𐿈'
            >>> Chorasmian._to_numeral(10)
            '𐿉'
            >>> Chorasmian._to_numeral(11)
            '𐿅𐿉'
            >>> Chorasmian._to_numeral(100)
            '𐿋'
            >>> Chorasmian._to_numeral(123)
            '𐿇𐿊𐿋'
        """
        return reversed_greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Chorasmian numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> Chorasmian._from_numeral('𐿅')
            1
            >>> Chorasmian._from_numeral('𐿈')
            4
            >>> Chorasmian._from_numeral('𐿅𐿈')
            5
            >>> Chorasmian._from_numeral('𐿉')
            10
            >>> Chorasmian._from_numeral('𐿅𐿉')
            11
            >>> Chorasmian._from_numeral('𐿋')
            100
            >>> Chorasmian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Chorasmian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
