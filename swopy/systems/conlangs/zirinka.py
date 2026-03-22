"""Zirinka numeral system converters.

This module implements numeral systems from the Zirinka conlang.
Currently supports:

    Zirinka   U+E354-U+E35B  (Private Use Area)

Zirinka uses a positional base-8 (octal) encoding with eight unique digit
glyphs assigned from the UCSUR Private Use Area block U+E340-U+E35F.  Each
digit position is a power of 8; numbers are written most-significant digit
first (left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE354


class Zirinka(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Zirinka
    numerals.

    - Uses Unicode Private Use Area U+E354-U+E35B (UCSUR block U+E340-U+E35F)
    - The system is positional in base 8 with 8 unique digit glyphs

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

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(8)}
    _from_numeral_map: Mapping[str, int] = {chr(_ZERO + i): i for i in range(8)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Zirinka numerals.

        Examples:
            >>> Zirinka._to_numeral(0)
            '\ue354'
            >>> Zirinka._to_numeral(1)
            '\ue355'
            >>> Zirinka._to_numeral(42)
            '\ue359\ue356'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 8)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Zirinka numeral string to a non-negative integer.

        Examples:
            >>> Zirinka._from_numeral('\ue354')
            0
            >>> Zirinka._from_numeral('\ue355')
            1
            >>> Zirinka._from_numeral('\ue359\ue356')
            42
            >>> Zirinka._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Zirinka character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 8)
