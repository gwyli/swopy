"""Turkic numeral system converters.

This module implements numeral systems from the Turkic script family.
Currently supports:

    OldHungarian  U+10CFA-U+10CFF

Old Hungarian is a child script of Orkhon Turkic.  It is a purely additive
system written right-to-left (largest denomination on the right).  Encoding
uses greedy decomposition followed by reversal; decoding reverses the input
before summing.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class OldHungarian(System[str, int]):
    """Implements bidirectional conversion between integers and Old Hungarian numerals.

    - Uses Unicode block U+10CFA-U+10CFF (six glyphs: 1, 5, 10, 50, 100, 1000)
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
        1000: "\U00010cff",  # 𐳿 OLD HUNGARIAN CAPITAL LETTER US (1000)
        100: "\U00010cfe",  # 𐳾 OLD HUNGARIAN CAPITAL LETTER EC (100)
        50: "\U00010cfd",  # 𐳽 OLD HUNGARIAN CAPITAL LETTER OLY (50)
        10: "\U00010cfc",  # 𐳼 OLD HUNGARIAN CAPITAL LETTER ENT (10)
        5: "\U00010cfb",  # 𐳻 OLD HUNGARIAN CAPITAL LETTER EY (5)
        1: "\U00010cfa",  # 𐳺 OLD HUNGARIAN CAPITAL LETTER EJ (1)
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Old Hungarian numerals.

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> OldHungarian._to_numeral(1)
            '𐳺'
            >>> OldHungarian._to_numeral(5)
            '𐳻'
            >>> OldHungarian._to_numeral(10)
            '𐳼'
            >>> OldHungarian._to_numeral(50)
            '𐳽'
            >>> OldHungarian._to_numeral(100)
            '𐳾'
            >>> OldHungarian._to_numeral(1000)
            '𐳿'
            >>> OldHungarian._to_numeral(7)
            '𐳺𐳺𐳻'
            >>> OldHungarian._to_numeral(1999)
            '𐳺𐳺𐳺𐳺𐳻𐳼𐳼𐳼𐳼𐳽𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳿'
        """
        return reversed_greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Old Hungarian numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> OldHungarian._from_numeral('𐳺')
            1
            >>> OldHungarian._from_numeral('𐳻')
            5
            >>> OldHungarian._from_numeral('𐳼')
            10
            >>> OldHungarian._from_numeral('𐳽')
            50
            >>> OldHungarian._from_numeral('𐳾')
            100
            >>> OldHungarian._from_numeral('𐳿')
            1000
            >>> OldHungarian._from_numeral('𐳺𐳺𐳻')
            7
            >>> OldHungarian._from_numeral('𐳺𐳺𐳺𐳺𐳻𐳼𐳼𐳼𐳼𐳽𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳾𐳿')
            1999
            >>> OldHungarian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid OldHungarian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
