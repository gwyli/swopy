"""Ewellic numeral system converters.

This module implements numeral systems from the Ewellic conlang.
Currently supports:

    Ewellic   U+E6C0-U+E6CF  (Private Use Area)

Ewellic uses a positional base-16 (hexadecimal) encoding with sixteen unique
digit glyphs assigned from the UCSUR Private Use Area block U+E680-U+E6CF.
Digits 0-9 map to U+E6C0-U+E6C9, and hex digits 10-15 map to U+E6CA-U+E6CF.
Numbers are written most-significant digit first (left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE6C0


class Ewellic(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Ewellic
    numerals.

    - Uses Unicode Private Use Area U+E6C0-U+E6CF (UCSUR block U+E680-U+E6CF)
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
        """Convert a non-negative integer to Ewellic numerals.

        Examples:
            >>> Ewellic._to_numeral(0)
            '\ue6c0'
            >>> Ewellic._to_numeral(1)
            '\ue6c1'
            >>> Ewellic._to_numeral(42)
            '\ue6c2\ue6ca'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 16)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ewellic numeral string to a non-negative integer.

        Examples:
            >>> Ewellic._from_numeral('\ue6c0')
            0
            >>> Ewellic._from_numeral('\ue6c1')
            1
            >>> Ewellic._from_numeral('\ue6c2\ue6ca')
            42
            >>> Ewellic._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Ewellic character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 16)
