"""Olaetyan numeral system converters.

This module implements numeral systems from the Olaetyan conlang.
Currently supports:

    Olaetyan   U+E3E9-U+E3F2  (Private Use Area)

Olaetyan uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+E3B0-U+E3FF.  Each digit
position is a power of 10; numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_DIGITS = [0xE3E9 + i for i in range(10)]


class Olaetyan(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Olaetyan
    numerals.

    - Uses Unicode Private Use Area U+E3E9-U+E3F2 (UCSUR block U+E3B0-U+E3FF)
    - The system is positional in base 10 with 10 unique digit glyphs

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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xE3E9 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {chr(0xE3E9 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Olaetyan numerals.

        Examples:
            >>> Olaetyan._to_numeral(0)
            '\ue3e9'
            >>> Olaetyan._to_numeral(1)
            '\ue3ea'
            >>> Olaetyan._to_numeral(42)
            '\ue3ed\ue3eb'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Olaetyan numeral string to a non-negative integer.

        Examples:
            >>> Olaetyan._from_numeral('\ue3e9')
            0
            >>> Olaetyan._from_numeral('\ue3ea')
            1
            >>> Olaetyan._from_numeral('\ue3ed\ue3eb')
            42
            >>> Olaetyan._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Olaetyan character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
