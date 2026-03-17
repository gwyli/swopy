"""Sogdian and related numeral system converters.

This module implements numeral systems from the Sogdian script family and
related Middle Iranian scripts.
Currently supports:

    Manichaean  U+10AC0-U+10AFF  (five glyphs: 1, 5, 10, 20, 100)
    Old Sogdian U+10F00-U+10F2F  (nine glyphs: 1, 2, 3, 4, 5, 10, 20, 30, 100)
    Sogdian     U+10F30-U+10F6F  (four glyphs: 1, 10, 20, 100)

All three systems are purely additive and written right-to-left (largest
denomination on the right).  Encoding uses greedy decomposition followed by
reversal; decoding reverses the input before summing.
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class Manichaean(System[str, int]):
    """Manichaean numeral system converter.

    Implements bidirectional conversion between integers and Manichaean numeral
    strings using Unicode block U+10AC0–U+10AFF. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 5, 10, 20, and 100. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010aef",  # 𐫯 MANICHAEAN NUMBER ONE HUNDRED
        20: "\U00010aee",  # 𐫮 MANICHAEAN NUMBER TWENTY
        10: "\U00010aed",  # 𐫭 MANICHAEAN NUMBER TEN
        5: "\U00010aec",  # 𐫬 MANICHAEAN NUMBER FIVE
        1: "\U00010aeb",  # 𐫫 MANICHAEAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Manichaean numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Manichaean._to_numeral(1)
            '𐫫'
            >>> Manichaean._to_numeral(5)
            '𐫬'
            >>> Manichaean._to_numeral(10)
            '𐫭'
            >>> Manichaean._to_numeral(11)
            '𐫫𐫭'
            >>> Manichaean._to_numeral(25)
            '𐫬𐫮'
            >>> Manichaean._to_numeral(100)
            '𐫯'
            >>> Manichaean._to_numeral(999)
            '𐫫𐫫𐫫𐫫𐫬𐫭𐫮𐫮𐫮𐫮𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Manichaean numeral string to its Arabic integer value.

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
            >>> Manichaean._from_numeral('𐫫')
            1
            >>> Manichaean._from_numeral('𐫬')
            5
            >>> Manichaean._from_numeral('𐫭')
            10
            >>> Manichaean._from_numeral('𐫫𐫭')
            11
            >>> Manichaean._from_numeral('𐫬𐫮')
            25
            >>> Manichaean._from_numeral('𐫯')
            100
            >>> Manichaean._from_numeral('𐫫𐫫𐫫𐫫𐫬𐫭𐫮𐫮𐫮𐫮𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯')
            999
            >>> Manichaean._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Manichaean character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class OldSogdian(System[str, int]):
    """Old Sogdian numeral system converter.

    Implements bidirectional conversion between integers and Old Sogdian numeral
    strings using Unicode block U+10F00–U+10F2F. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 2, 3, 4, 5, 10, 20, 30, and 100. The valid range
    is 1–999. (U+10F26 NUMBER ONE HALF is excluded.)

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010f25",  # 𐼥 OLD SOGDIAN NUMBER ONE HUNDRED
        30: "\U00010f24",  # 𐼤 OLD SOGDIAN NUMBER THIRTY
        20: "\U00010f23",  # 𐼣 OLD SOGDIAN NUMBER TWENTY
        10: "\U00010f22",  # 𐼢 OLD SOGDIAN NUMBER TEN
        5: "\U00010f21",  # 𐼡 OLD SOGDIAN NUMBER FIVE
        4: "\U00010f20",  # 𐼠 OLD SOGDIAN NUMBER FOUR
        3: "\U00010f1f",  # 𐼟 OLD SOGDIAN NUMBER THREE
        2: "\U00010f1e",  # 𐼞 OLD SOGDIAN NUMBER TWO
        1: "\U00010f1d",  # 𐼝 OLD SOGDIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Old Sogdian numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> OldSogdian._to_numeral(1)
            '𐼝'
            >>> OldSogdian._to_numeral(5)
            '𐼡'
            >>> OldSogdian._to_numeral(10)
            '𐼢'
            >>> OldSogdian._to_numeral(30)
            '𐼤'
            >>> OldSogdian._to_numeral(100)
            '𐼥'
            >>> OldSogdian._to_numeral(999)
            '𐼠𐼡𐼤𐼤𐼤𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Old Sogdian numeral string to its Arabic integer value.

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
            >>> OldSogdian._from_numeral('𐼝')
            1
            >>> OldSogdian._from_numeral('𐼡')
            5
            >>> OldSogdian._from_numeral('𐼢')
            10
            >>> OldSogdian._from_numeral('𐼤')
            30
            >>> OldSogdian._from_numeral('𐼥')
            100
            >>> OldSogdian._from_numeral('𐼠𐼡𐼤𐼤𐼤𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥')
            999
            >>> OldSogdian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid OldSogdian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class Sogdian(System[str, int]):
    """Sogdian numeral system converter.

    Implements bidirectional conversion between integers and Sogdian numeral
    strings using Unicode block U+10F30–U+10F6F. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 10, 20, and 100. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010f54",  # 𐽔 SOGDIAN NUMBER ONE HUNDRED
        20: "\U00010f53",  # 𐽓 SOGDIAN NUMBER TWENTY
        10: "\U00010f52",  # 𐽒 SOGDIAN NUMBER TEN
        1: "\U00010f51",  # 𐽑 SOGDIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Sogdian numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Sogdian._to_numeral(1)
            '𐽑'
            >>> Sogdian._to_numeral(10)
            '𐽒'
            >>> Sogdian._to_numeral(20)
            '𐽓'
            >>> Sogdian._to_numeral(21)
            '𐽑𐽓'
            >>> Sogdian._to_numeral(100)
            '𐽔'
            >>> Sogdian._to_numeral(999)
            '𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽒𐽓𐽓𐽓𐽓𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Sogdian numeral string to its Arabic integer value.

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
            >>> Sogdian._from_numeral('𐽑')
            1
            >>> Sogdian._from_numeral('𐽒')
            10
            >>> Sogdian._from_numeral('𐽓')
            20
            >>> Sogdian._from_numeral('𐽑𐽓')
            21
            >>> Sogdian._from_numeral('𐽔')
            100
            >>> Sogdian._from_numeral('𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽒𐽓𐽓𐽓𐽓𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔')
            999
            >>> Sogdian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Sogdian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
