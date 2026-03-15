"""Mongolian and related numeral system converters.

This module implements numeral systems from the Mongolian cultural sphere.
Currently supports:

    Khitan Small Script  U+18B00-U+18CFF  (specific glyphs listed below)

Khitan is a multiplicative-additive system with myriad (10,000) grouping.
Digits 1-9 have unique glyphs; multipliers for 10, 100, 1,000 and 10,000
are separate characters. Zero is omitted from normal use (place values are
simply skipped when their digit is zero).

Encoding rules:

    All places  - digit 1 is omitted before every multiplier (including tens)
    Myriad      - the full sub-myriad coefficient (1-9999) precedes [x10000];
                  the coefficient is omitted entirely when equal to 1
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_myriad_from_numeral,
    multiplicative_myriad_to_numeral,
)


class Khitan(System[str, int]):
    """Khitan numeral system converter.

    Implements bidirectional conversion between integers and Khitan Small
    Script numeral strings. The system is multiplicative-additive with a
    myriad base:

    - Digits 1-9 are represented by unique glyphs (U+18B00-U+18B08).
    - Multipliers x10, x100, x1000, x10000 are separate characters.
    - The digit 1 is always omitted before every multiplier (including tens).
    - Zero places are skipped entirely (no zero glyph in normal use).
    - The myriad (x10000) coefficient can itself be a sub-myriad number
      (2-9999); a coefficient of 1 is omitted entirely.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999,999).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999

    encodings: ClassVar[Encodings] = {"utf8"}

    # Individual digit glyphs (1-9): U+18B00-U+18B08
    _to_numeral_map: Mapping[int, str] = {i: chr(0x18B00 + i - 1) for i in range(1, 10)}

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    # Multiplier glyphs (largest first)
    _multiplier_map: ClassVar[Mapping[int, str]] = {
        10000: "\U00018b0c",  # Khitan myriad (x10,000)
        1000: "\U00018b0b",  # Khitan thousand (x1,000)
        100: "\U00018b09",  # Khitan hundred (x100)
        10: "\U00018b0a",  # Khitan ten (x10)
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Khitan numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + myriad``,
        where a coefficient of 1 is omitted and coefficients 2-9999 are
        encoded as sub-myriad numbers. The remainder (0-9999) is appended
        directly.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Khitan._to_numeral(1)
            '\U00018b00'
            >>> Khitan._to_numeral(10)
            '\U00018b0a'
            >>> Khitan._to_numeral(12)
            '\U00018b0a\U00018b01'
            >>> Khitan._to_numeral(100)
            '\U00018b09'
            >>> Khitan._to_numeral(10000)
            '\U00018b0c'
            >>> Khitan._to_numeral(100000)
            '\U00018b0a\U00018b0c'
            >>> Khitan._to_numeral(20000)
            '\U00018b01\U00018b0c'
        """
        return multiplicative_myriad_to_numeral(
            number,
            cls._to_numeral_map,
            cls._multiplier_map,
            explicit_one_tens=False,
        )

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Khitan numeral string to its Arabic integer value.

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
            >>> Khitan._from_numeral('\U00018b00')
            1
            >>> Khitan._from_numeral('\U00018b0a')
            10
            >>> Khitan._from_numeral('\U00018b0a\U00018b01')
            12
            >>> Khitan._from_numeral('\U00018b09')
            100
            >>> Khitan._from_numeral('\U00018b0c')
            10000
            >>> Khitan._from_numeral('\U00018b0a\U00018b0c')
            100000
            >>> Khitan._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Khitan character: '?'
        """
        return multiplicative_myriad_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls._multiplier_from_map,
            cls.__name__,
        )
