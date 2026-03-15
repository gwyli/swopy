"""Semitic numeral system converters.

This module implements numeral systems from ancient Semitic cultures.
Currently supports:

    Old South Arabian  U+10A60-U+10A7F  (specific glyphs listed below)
    Old North Arabian  U+10A80-U+10A9F  (specific glyphs listed below)

Both systems are purely additive, using greedy decomposition for encoding
and character-sum for decoding.

Old South Arabian uses an acrophonic system where certain letters double as
numerals (e.g. Alef for 1000, Ayn for 10000), alongside two dedicated numeral
characters (Number One, Number Fifty).

Old North Arabian has three dedicated numeral characters covering values
1, 10, and 20.
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class AncientSouthArabian(System[str, int]):
    """Ancient South Arabian numeral system converter.

    Implements bidirectional conversion between integers and Old South Arabian
    numeral strings using Unicode block U+10A60–U+10A7F. The system is purely
    additive with five signs:

    - 𐩲  U+10A72  LETTER AYN      (acrophonic)  ->  10,000
    - 𐩱  U+10A71  LETTER ALEF     (acrophonic)  ->   1,000
    - 𐩣  U+10A63  LETTER MEM      (acrophonic)  ->     100
    - 𐩾  U+10A7E  NUMBER FIFTY                  ->      50
    - 𐩽  U+10A7D  NUMBER ONE                    ->       1

    Values between signs are expressed by repetition (e.g. 3 = 𐩽𐩽𐩽,
    200 = 𐩣𐩣). The valid range is 1–99,999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        10000: "\U00010a72",  # 𐩲  LETTER AYN      (acrophonic numeral)
        1000: "\U00010a71",  # 𐩱  LETTER ALEF     (acrophonic numeral)
        100: "\U00010a63",  # 𐩣  LETTER MEM      (acrophonic numeral)
        50: "\U00010a7e",  # 𐩾  NUMBER FIFTY
        1: "\U00010a7d",  # 𐩽  NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Ancient South Arabian numeral
        representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> AncientSouthArabian._to_numeral(1)
            '𐩽'
            >>> AncientSouthArabian._to_numeral(3)
            '𐩽𐩽𐩽'
            >>> AncientSouthArabian._to_numeral(50)
            '𐩾'
            >>> AncientSouthArabian._to_numeral(100)
            '𐩣'
            >>> AncientSouthArabian._to_numeral(1000)
            '𐩱'
            >>> AncientSouthArabian._to_numeral(10000)
            '𐩲'
            >>> AncientSouthArabian._to_numeral(31000)
            '𐩲𐩲𐩲𐩱'
            >>> AncientSouthArabian._to_numeral(40000)
            '𐩲𐩲𐩲𐩲'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ancient South Arabian numeral string to its Arabic integer value.

        Sums the values of each glyph in the string.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> AncientSouthArabian._from_numeral('𐩽')
            1
            >>> AncientSouthArabian._from_numeral('𐩾')
            50
            >>> AncientSouthArabian._from_numeral('𐩣')
            100
            >>> AncientSouthArabian._from_numeral('𐩱')
            1000
            >>> AncientSouthArabian._from_numeral('𐩲')
            10000
            >>> AncientSouthArabian._from_numeral('𐩲𐩲𐩲𐩱')
            31000
            >>> AncientSouthArabian._from_numeral('𐩲𐩲𐩲𐩲')
            40000
            >>> AncientSouthArabian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid AncientSouthArabian character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class AncientNorthArabian(System[str, int]):
    """Ancient North Arabian numeral system converter.

    Implements bidirectional conversion between integers and Old North Arabian
    numeral strings using Unicode block U+10A80–U+10A9F. The system is purely
    additive with three dedicated numeral signs:

    - 𐪟  U+10A9F  NUMBER TWENTY  ->  20
    - 𐪞  U+10A9E  NUMBER TEN     ->  10
    - 𐪝  U+10A9D  NUMBER ONE     ->   1

    Values between signs are expressed by repetition (e.g. 3 = 𐪝𐪝𐪝,
    30 = 𐪟𐪞). The valid range is 1–99.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        20: "\U00010a9f",  # 𐪟  NUMBER TWENTY
        10: "\U00010a9e",  # 𐪞  NUMBER TEN
        1: "\U00010a9d",  # 𐪝  NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Ancient North Arabian numeral
        representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> AncientNorthArabian._to_numeral(1)
            '𐪝'
            >>> AncientNorthArabian._to_numeral(9)
            '𐪝𐪝𐪝𐪝𐪝𐪝𐪝𐪝𐪝'
            >>> AncientNorthArabian._to_numeral(10)
            '𐪞'
            >>> AncientNorthArabian._to_numeral(20)
            '𐪟'
            >>> AncientNorthArabian._to_numeral(30)
            '𐪟𐪞'
            >>> AncientNorthArabian._to_numeral(99)
            '𐪟𐪟𐪟𐪟𐪞𐪝𐪝𐪝𐪝𐪝𐪝𐪝𐪝𐪝'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ancient North Arabian numeral string to its Arabic integer value.

        Sums the values of each glyph in the string.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> AncientNorthArabian._from_numeral('𐪝')
            1
            >>> AncientNorthArabian._from_numeral('𐪞')
            10
            >>> AncientNorthArabian._from_numeral('𐪟')
            20
            >>> AncientNorthArabian._from_numeral('𐪟𐪞')
            30
            >>> AncientNorthArabian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid AncientNorthArabian character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
