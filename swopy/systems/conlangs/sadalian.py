"""Sadalian numeral system converters.

This module implements numeral systems from the Sadalian conlang.
Currently supports:

    Sadalian   U+F2670-U+F267F  (Private Use Area)

Sadalian uses a positional base-16 (hexadecimal) encoding with sixteen unique
digit glyphs assigned from the UCSUR Private Use Area block U+F2000-U+F267F.
Digits 0-15 map to U+F2670-U+F267F.  Numbers are written most-significant
digit first (left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xF2670


class Sadalian(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Sadalian
    numerals.

    - Uses Unicode Private Use Area U+F2670-U+F267F (UCSUR block U+F2000-U+F267F)
    - The system is positional in base 16 with 16 unique digit glyphs (0-15)

    Attributes:
        minimum: Minimum valid value (0)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False - no upper bound exists
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(16)}
    _from_numeral_map: Mapping[str, int] = {chr(_ZERO + i): i for i in range(16)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Sadalian numerals.

        Examples:
            >>> Sadalian._to_numeral(0)
            '\U000f2670'
            >>> Sadalian._to_numeral(1)
            '\U000f2671'
            >>> Sadalian._to_numeral(42)
            '\U000f2672\U000f267a'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 16)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Sadalian numeral string to a non-negative integer.

        Examples:
            >>> Sadalian._from_numeral('\U000f2670')
            0
            >>> Sadalian._from_numeral('\U000f2671')
            1
            >>> Sadalian._from_numeral('\U000f2672\U000f267a')
            42
            >>> Sadalian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Sadalian character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 16)
