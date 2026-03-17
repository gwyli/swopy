# ruff: noqa: RUF002
"""Numeric notation system converters.

This module implements generic numeric notation systems not tied to a single
cultural script family.
Currently supports:

    Counting Rod Numerals  U+1D360-U+1D371  (eighteen glyphs: unit digits 1–9,
                                              tens digits 10–90)

Counting Rod is a purely additive system that encodes each decimal place with a
dedicated glyph: nine unit-digit glyphs (1–9) for the ones place and nine
tens-digit glyphs (10–90) for the tens place.  Numbers are encoded as
(optional tens glyph)(optional unit glyph).  Greedy decomposition is used for
encoding and character-sum for decoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class CountingRod(System[str, int]):
    """Counting Rod numeral system converter.

    Implements bidirectional conversion between integers and Counting Rod numeral
    strings using Unicode block U+1D360-U+1D371. The system encodes each decimal
    place with a dedicated glyph: nine unit-digit glyphs (1-9) for the ones place
    and nine tens-digit glyphs (10-90) for the tens place.

    Numbers are encoded as (optional tens glyph)(optional unit glyph), e.g.
    11 = 𝍩𝍠 (tens-digit-1 + unit-digit-1). Multiples of 10 omit the unit glyph.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        90: "\U0001d371",  # 𝍱  COUNTING ROD TENS DIGIT NINE
        80: "\U0001d370",  # 𝍰  COUNTING ROD TENS DIGIT EIGHT
        70: "\U0001d36f",  # 𝍯  COUNTING ROD TENS DIGIT SEVEN
        60: "\U0001d36e",  # 𝍮  COUNTING ROD TENS DIGIT SIX
        50: "\U0001d36d",  # 𝍭  COUNTING ROD TENS DIGIT FIVE
        40: "\U0001d36c",  # 𝍬  COUNTING ROD TENS DIGIT FOUR
        30: "\U0001d36b",  # 𝍫  COUNTING ROD TENS DIGIT THREE
        20: "\U0001d36a",  # 𝍪  COUNTING ROD TENS DIGIT TWO
        10: "\U0001d369",  # 𝍩  COUNTING ROD TENS DIGIT ONE
        9: "\U0001d368",  # 𝍨  COUNTING ROD UNIT DIGIT NINE
        8: "\U0001d367",  # 𝍧  COUNTING ROD UNIT DIGIT EIGHT
        7: "\U0001d366",  # 𝍦  COUNTING ROD UNIT DIGIT SEVEN
        6: "\U0001d365",  # 𝍥  COUNTING ROD UNIT DIGIT SIX
        5: "\U0001d364",  # 𝍤  COUNTING ROD UNIT DIGIT FIVE
        4: "\U0001d363",  # 𝍣  COUNTING ROD UNIT DIGIT FOUR
        3: "\U0001d362",  # 𝍢  COUNTING ROD UNIT DIGIT THREE
        2: "\U0001d361",  # 𝍡  COUNTING ROD UNIT DIGIT TWO
        1: "\U0001d360",  # 𝍠  COUNTING ROD UNIT DIGIT ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Counting Rod numeral representation.

        Encodes the tens place with a tens-digit glyph (if non-zero) followed by
        the units place with a unit-digit glyph (if non-zero).

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> CountingRod._to_numeral(1)
            '𝍠'
            >>> CountingRod._to_numeral(9)
            '𝍨'
            >>> CountingRod._to_numeral(10)
            '𝍩'
            >>> CountingRod._to_numeral(11)
            '𝍩𝍠'
            >>> CountingRod._to_numeral(50)
            '𝍭'
            >>> CountingRod._to_numeral(99)
            '𝍱𝍨'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Counting Rod numeral string to its Arabic integer value.

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
            >>> CountingRod._from_numeral('𝍠')
            1
            >>> CountingRod._from_numeral('𝍨')
            9
            >>> CountingRod._from_numeral('𝍩')
            10
            >>> CountingRod._from_numeral('𝍩𝍠')
            11
            >>> CountingRod._from_numeral('𝍱𝍨')
            99
            >>> CountingRod._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid CountingRod character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
