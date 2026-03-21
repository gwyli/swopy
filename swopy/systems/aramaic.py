"""Aramaic numeral system converters.

This module implements numeral systems from the Aramaic script family.

Currently supports:

    Palmyrene        U+10860-U+1087F
    Hatran           U+108E0-U+108FF
    Imperial Aramaic U+10840-U+1085F

Palmyrene and Hatran are purely additive left-to-right systems using greedy
decomposition for encoding and character-sum for decoding.

Imperial Aramaic is purely additive but written right-to-left (largest
denomination on the right): encoding reverses the greedy result, and
decoding reverses the input before summing.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class Palmyrene(System[str, int]):
    """Implements bidirectional conversion between integers and Palmyrene numerals.

    - Uses Unicode block U+10860-U+1087F
    - The system is purely additive with dedicated signs for 1, 2, 3, 4, 5, 10, and 20

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (99)
        maximum_is_many: False - Integers greater than 99 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        20: "\U0001087f",  # 𐡿 PALMYRENE NUMBER TWENTY
        10: "\U0001087e",  # 𐡾 PALMYRENE NUMBER TEN
        5: "\U0001087d",  # 𐡽 PALMYRENE NUMBER FIVE
        4: "\U0001087c",  # 𐡼 PALMYRENE NUMBER FOUR
        3: "\U0001087b",  # 𐡻 PALMYRENE NUMBER THREE
        2: "\U0001087a",  # 𐡺 PALMYRENE NUMBER TWO
        1: "\U00010879",  # 𐡹 PALMYRENE NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Palmyrene numerals.

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> Palmyrene._to_numeral(1)
            '𐡹'
            >>> Palmyrene._to_numeral(15)
            '𐡾𐡽'
            >>> Palmyrene._to_numeral(20)
            '𐡿'
            >>> Palmyrene._to_numeral(21)
            '𐡿𐡹'
            >>> Palmyrene._to_numeral(99)
            '𐡿𐡿𐡿𐡿𐡾𐡽𐡼'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Palmyrene numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> Palmyrene._from_numeral('𐡹')
            1
            >>> Palmyrene._from_numeral('𐡾𐡽')
            15
            >>> Palmyrene._from_numeral('𐡿')
            20
            >>> Palmyrene._from_numeral('𐡿𐡹')
            21
            >>> Palmyrene._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Palmyrene character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Hatran(System[str, int]):
    """Implements bidirectional conversion between integers and Hatran numerals.

    - Uses Unicode block U+108E0-U+108FF
    - The system is purely additive with dedicated signs for 1, 5, 10, 20, and 100

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (999)
        maximum_is_many: False - Integers greater than 999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        100: "\U000108ff",  # 𐣿 HATRAN NUMBER ONE HUNDRED
        20: "\U000108fe",  # 𐣾 HATRAN NUMBER TWENTY
        10: "\U000108fd",  # 𐣽 HATRAN NUMBER TEN
        5: "\U000108fc",  # 𐣼 HATRAN NUMBER FIVE
        1: "\U000108fb",  # 𐣻 HATRAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Hatran numerals.

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> Hatran._to_numeral(1)
            '𐣻'
            >>> Hatran._to_numeral(6)
            '𐣼𐣻'
            >>> Hatran._to_numeral(100)
            '𐣿'
            >>> Hatran._to_numeral(125)
            '𐣿𐣾𐣼'
            >>> Hatran._to_numeral(999)
            '𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣾𐣾𐣾𐣾𐣽𐣼𐣻𐣻𐣻𐣻'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Hatran numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> Hatran._from_numeral('𐣻')
            1
            >>> Hatran._from_numeral('𐣼𐣻')
            6
            >>> Hatran._from_numeral('𐣿')
            100
            >>> Hatran._from_numeral('𐣿𐣾𐣼')
            125
            >>> Hatran._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Hatran character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class ImperialAramaic(System[str, int]):
    """Implements bidirectional conversion between integers and Imperial Aramaic
    numerals.

    - Uses Unicode block U+10840-U+1085F
    - The system is purely additive and written right-to-left (largest denomination on
        the right), with dedicated signs for 1, 2, 3, 10, 20, 100, 1000, and 10000.

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (99,999)
        maximum_is_many: False - Integers greater than 99 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        10000: "\U0001085f",  # 𐡟 IMPERIAL ARAMAIC NUMBER TEN THOUSAND
        1000: "\U0001085e",  # 𐡞 IMPERIAL ARAMAIC NUMBER ONE THOUSAND
        100: "\U0001085d",  # 𐡝 IMPERIAL ARAMAIC NUMBER ONE HUNDRED
        20: "\U0001085c",  # 𐡜 IMPERIAL ARAMAIC NUMBER TWENTY
        10: "\U0001085b",  # 𐡛 IMPERIAL ARAMAIC NUMBER TEN
        3: "\U0001085a",  # 𐡚 IMPERIAL ARAMAIC NUMBER THREE
        2: "\U00010859",  # 𐡙 IMPERIAL ARAMAIC NUMBER TWO
        1: "\U00010858",  # 𐡘 IMPERIAL ARAMAIC NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Imperial Aramaic numerals

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> ImperialAramaic._to_numeral(1)
            '𐡘'
            >>> ImperialAramaic._to_numeral(3)
            '𐡚'
            >>> ImperialAramaic._to_numeral(10)
            '𐡛'
            >>> ImperialAramaic._to_numeral(100)
            '𐡝'
            >>> ImperialAramaic._to_numeral(1000)
            '𐡞'
            >>> ImperialAramaic._to_numeral(10000)
            '𐡟'
            >>> ImperialAramaic._to_numeral(999)
            '𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝'
            >>> ImperialAramaic._to_numeral(99999)
            '𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡟𐡟𐡟𐡟𐡟𐡟𐡟𐡟𐡟'
        """
        return reversed_greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Imperial Aramaic numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> ImperialAramaic._from_numeral('𐡘')
            1
            >>> ImperialAramaic._from_numeral('𐡚')
            3
            >>> ImperialAramaic._from_numeral('𐡛')
            10
            >>> ImperialAramaic._from_numeral('𐡝')
            100
            >>> ImperialAramaic._from_numeral('𐡞')
            1000
            >>> ImperialAramaic._from_numeral('𐡟')
            10000
            >>> ImperialAramaic._from_numeral('𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝')
            999
            >>> ImperialAramaic._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid ImperialAramaic character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
