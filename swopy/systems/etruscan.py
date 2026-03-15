"""Etruscan numeral system converter.

This module implements the Etruscan numeral system, which uses an additive
combination of four glyphs to represent numbers. Etruscan numerals are read
right-to-left: the largest denomination appears on the right of the string.

Unicode glyphs (Old Italic Numeral block, U+10320–U+10323):

    𐌠  U+10320  ETRUSCAN NUMERAL ONE     →  1
    𐌡  U+10321  ETRUSCAN NUMERAL FIVE    →  5
    𐌢  U+10322  ETRUSCAN NUMERAL TEN     →  10
    𐌣  U+10323  ETRUSCAN NUMERAL FIFTY   →  50

The valid range is 1–399, which covers all values expressible with these four
glyphs and reflects the attested epigraphic record.
"""

# Ignore ambiguous unicode character strings in Etruscan numerals
# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class Etruscan(System[str, int]):
    """Etruscan numeral system converter.

    Implements bidirectional conversion between integers and Etruscan numeral strings.

    Etruscan numerals are a purely additive system written right-to-left (largest
    denomination on the right).  ``_to_numeral`` builds numerals using a greedy
    decomposition (largest denomination first) and reverses the result so that
    the highest-denomination glyphs appear on the right.  ``_from_numeral``
    reverses the input string before summing, so both paths share the same
    left-to-right internal iteration.

    Attributes:
        to_numeral_map: Mapping of integer values to Etruscan numeral components,
            ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Etruscan numeral characters to their integer
            values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (399), limited by Etruscan numeral notation.
        maximum_is_many: False, as 399 is a precise limit.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 399

    _to_numeral_map: Mapping[int, str] = {
        50: "\U00010323",  # 𐌣 - OLD ITALIC NUMERAL FIFTY
        10: "\U00010322",  # 𐌢 - OLD ITALIC NUMERAL TEN
        5: "\U00010321",  # 𐌡 - OLD ITALIC NUMERAL FIVE
        1: "\U00010320",  # 𐌠 - OLD ITALIC NUMERAL ONE
    }

    _from_numeral_map: Mapping[str, int] = {
        "\U00010320": 1,
        "\U00010321": 5,
        "\U00010322": 10,
        "\U00010323": 50,
        "I": 1,
        "Λ": 5,
        "X": 10,
        "↑": 50,
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Etruscan numeral representation.

        Uses a greedy decomposition (largest denomination first), then reverses
        the result so the highest-denomination glyphs appear on the right, in
        keeping with the Etruscan right-to-left writing convention.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Etruscan._to_numeral(1)
            '𐌠'
            >>> Etruscan._to_numeral(4)
            '𐌠𐌠𐌠𐌠'
            >>> Etruscan._to_numeral(6)
            '𐌠𐌡'
            >>> Etruscan._to_numeral(10)
            '𐌢'
            >>> Etruscan._to_numeral(17)
            '𐌠𐌠𐌡𐌢'
            >>> Etruscan._to_numeral(29)
            '𐌠𐌠𐌠𐌠𐌡𐌢𐌢'
            >>> Etruscan._to_numeral(55)
            '𐌡𐌣'
            >>> Etruscan._to_numeral(399)
            '𐌠𐌠𐌠𐌠𐌡𐌢𐌢𐌢𐌢𐌣𐌣𐌣𐌣𐌣𐌣𐌣'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Etruscan numeral string to its Arabic integer value.

        Accepts both Unicode glyphs (e.g. ``'𐌠𐌡'``) and their ASCII equivalents
        (e.g. ``'IΛ'``).  The string is expected in standard right-to-left reading
        order (largest denomination on the right), so it is reversed internally
        before summing.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Etruscan._from_numeral('𐌠𐌠𐌠𐌠')
            4
            >>> Etruscan._from_numeral('𐌠𐌡')
            6
            >>> Etruscan._from_numeral('𐌠𐌠𐌡𐌢')
            17
            >>> Etruscan._from_numeral('𐌠𐌠𐌠𐌠𐌡𐌢𐌢')
            29
            >>> Etruscan._from_numeral('IIΛX')
            17
            >>> Etruscan._from_numeral('IIIIΛXX')
            29
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
