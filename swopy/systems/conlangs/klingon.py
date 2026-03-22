"""Klingon numeral system converters.

This module implements numeral systems from the Klingon conlang.
Currently supports:

    Klingon   U+F8F0-U+F8F9  (Private Use Area)

Klingon uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area Klingon block U+F8D0-U+F8FF.  Each
digit position is a power of 10; numbers are written most-significant digit
first (left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Klingon(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Klingon
    numerals.

    - Uses Unicode Private Use Area U+F8F0-U+F8F9 (UCSUR Klingon block U+F8D0-U+F8FF)
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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xF8F0 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {chr(0xF8F0 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Klingon numerals.

        Examples:
            >>> Klingon._to_numeral(0)
            '\uf8f0'
            >>> Klingon._to_numeral(1)
            '\uf8f1'
            >>> Klingon._to_numeral(42)
            '\uf8f4\uf8f2'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Klingon numeral string to a non-negative integer.

        Examples:
            >>> Klingon._from_numeral('\uf8f0')
            0
            >>> Klingon._from_numeral('\uf8f1')
            1
            >>> Klingon._from_numeral('\uf8f4\uf8f2')
            42
            >>> Klingon._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Klingon character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
