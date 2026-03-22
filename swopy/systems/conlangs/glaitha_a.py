"""Glaitha-A numeral system converters.

This module implements numeral systems from the Glaitha-A conlang.
Currently supports:

    GlaithaA   U+E910-U+E91F  (Private Use Area)

Glaitha-A uses a positional base-16 (hexadecimal) encoding with sixteen
unique digit glyphs assigned from the UCSUR Private Use Area block
U+E900-U+E97F.  Digits 0-9 map to U+E910-U+E919 and hex digits 10-15 map to
U+E91A-U+E91F.  Numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE910


class GlaithaA(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Glaitha-A
    numerals.

    - Uses Unicode Private Use Area U+E910-U+E91F (UCSUR block U+E900-U+E97F)
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
        """Convert a non-negative integer to Glaitha-A numerals.

        Examples:
            >>> GlaithaA._to_numeral(0)
            '\ue910'
            >>> GlaithaA._to_numeral(1)
            '\ue911'
            >>> GlaithaA._to_numeral(42)
            '\ue912\ue91a'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 16)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Glaitha-A numeral string to a non-negative integer.

        Examples:
            >>> GlaithaA._from_numeral('\ue910')
            0
            >>> GlaithaA._from_numeral('\ue911')
            1
            >>> GlaithaA._from_numeral('\ue912\ue91a')
            42
            >>> GlaithaA._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid GlaithaA character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 16)
