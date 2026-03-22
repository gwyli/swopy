"""Deini numeral system converters.

This module implements numeral systems from the Deini conlang.
Currently supports:

    Deini   U+ED00-U+ED09  (Private Use Area)

Deini uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+ED00-U+ED3F.  Each digit
position is a power of 10; numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Deini(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Deini
    numerals.

    - Uses Unicode Private Use Area U+ED00-U+ED09 (UCSUR block U+ED00-U+ED3F)
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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xED00 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {chr(0xED00 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Deini numerals.

        Examples:
            >>> Deini._to_numeral(0)
            '\ued00'
            >>> Deini._to_numeral(1)
            '\ued01'
            >>> Deini._to_numeral(42)
            '\ued04\ued02'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Deini numeral string to a non-negative integer.

        Examples:
            >>> Deini._from_numeral('\ued00')
            0
            >>> Deini._from_numeral('\ued01')
            1
            >>> Deini._from_numeral('\ued04\ued02')
            42
            >>> Deini._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Deini character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
