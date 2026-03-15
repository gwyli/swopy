"""Tibetan and related numeral system converters.

This module implements numeral systems from the Tibetan cultural sphere.
Currently supports:

    Tangut  U+17000-U+187FF  (specific glyphs listed below)

Tangut is a multiplicative-additive system with myriad (10,000) grouping.
Digits 1-9 have unique glyphs; multipliers for 10, 100, 1,000 and 10,000
are separate characters. Zero is omitted from normal use (place values are
simply skipped when their digit is zero).

Encoding rules:

    Tens place  - digit always explicit, even for 1: e.g. 10 = [1][x10]
    Other places - digit 1 is omitted; digit 2-9 precedes the multiplier
    Myriad      - the full sub-myriad coefficient (1-9999) precedes [x10000]
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_myriad_from_numeral,
    multiplicative_myriad_to_numeral,
)


class Tangut(System[str, int]):
    """Tangut numeral system converter.

    Implements bidirectional conversion between integers and Tangut numeral
    strings. The system is multiplicative-additive with a myriad base:

    - Digits 1-9 are represented by unique glyphs.
    - Multipliers x10, x100, x1000, x10000 are separate characters.
    - The tens place always carries an explicit digit (including 1).
    - Hundreds, thousands and myriad coefficients omit the digit when it is 1.
    - Zero places are skipped entirely (no zero glyph in normal use).
    - The myriad (x10000) coefficient can itself be a sub-myriad number (1-9999).

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999,999).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999

    encodings: ClassVar[Encodings] = {"utf8"}

    # Individual digit glyphs (1-9)
    _to_numeral_map: Mapping[int, str] = {
        1: "\U00017f11",  # 𗼑  Tangut digit one
        2: "\U000180ae",  # 𘂮  Tangut digit two
        3: "\U00018555",  # 𘕕  Tangut digit three
        4: "\U00017943",  # 𗥃  Tangut digit four
        5: "\U000173c1",  # 𗏁  Tangut digit five
        6: "\U00017901",  # 𗤁  Tangut digit six
        7: "\U000175d9",  # 𗗙  Tangut digit seven
        8: "\U0001824b",  # 𘉋  Tangut digit eight
        9: "\U000178ad",  # 𗢭  Tangut digit nine
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    # Multiplier glyphs (largest first)
    _multiplier_map: ClassVar[Mapping[int, str]] = {
        10000: "\U00017457",  # 𗑗  Tangut myriad (x10,000)
        1000: "\U000170d4",  # 𗃔  Tangut thousand (x1,000)
        100: "\U000172da",  # 𗋚  Tangut hundred (x100)
        10: "\U00017c17",  # 𗰗  Tangut ten (x10)
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Tangut numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + myriad``,
        where the coefficient (1-9999) is itself encoded as a sub-myriad number.
        The remainder (0-9999) is appended directly.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Tangut._to_numeral(1)
            '𗼑'
            >>> Tangut._to_numeral(10)
            '𗼑𗰗'
            >>> Tangut._to_numeral(15)
            '𗼑𗰗𗏁'
            >>> Tangut._to_numeral(100)
            '𗋚'
            >>> Tangut._to_numeral(200)
            '𘂮𗋚'
            >>> Tangut._to_numeral(1005)
            '𗃔𗏁'
            >>> Tangut._to_numeral(10000)
            '𗼑𗑗'
            >>> Tangut._to_numeral(20000)
            '𘂮𗑗'
            >>> Tangut._to_numeral(100000)
            '𗼑𗰗𗑗'
            >>> Tangut._to_numeral(99999999)
            '𗢭𗃔𗢭𗋚𗢭𗰗𗢭𗑗𗢭𗃔𗢭𗋚𗢭𗰗𗢭'
        """
        return multiplicative_myriad_to_numeral(
            number,
            cls._to_numeral_map,
            cls._multiplier_map,
            explicit_one_tens=True,
        )

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Tangut numeral string to its Arabic integer value.

        Splits at the myriad glyph (if present): the portion before it is
        parsed as a sub-myriad coefficient and multiplied by 10,000; the
        portion after is parsed as the remainder. If no myriad glyph is
        present, the whole string is parsed as a sub-myriad number.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Tangut._from_numeral('𗼑')
            1
            >>> Tangut._from_numeral('𗼑𗰗')
            10
            >>> Tangut._from_numeral('𗼑𗰗𗏁')
            15
            >>> Tangut._from_numeral('𗋚')
            100
            >>> Tangut._from_numeral('𗃔𗏁')
            1005
            >>> Tangut._from_numeral('𗼑𗑗')
            10000
            >>> Tangut._from_numeral('𗼑𗰗𗑗')
            100000
            >>> Tangut._from_numeral('𗢭𗃔𗢭𗋚𗢭𗰗𗢭𗑗𗢭𗃔𗢭𗋚𗢭𗰗𗢭')
            99999999
            >>> Tangut._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Tangut character: '?'
        """
        return multiplicative_myriad_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls._multiplier_from_map,
            cls.__name__,
        )
