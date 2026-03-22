"""Kinya numeral system converters.

This module implements numeral systems from the Kinya conlang.
Currently supports:

    Kinya   U+E1A0-U+E1A9  (Private Use Area)

Kinya uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+E150-U+E1AF.  Each digit
position is a power of 10; numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Kinya(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Kinya
    numerals.

    - Uses Unicode Private Use Area U+E1A0-U+E1A9 (UCSUR block U+E150-U+E1AF)
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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xE1A0 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {chr(0xE1A0 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Kinya numerals.

        Examples:
            >>> Kinya._to_numeral(0)
            '\ue1a0'
            >>> Kinya._to_numeral(1)
            '\ue1a1'
            >>> Kinya._to_numeral(42)
            '\ue1a4\ue1a2'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Kinya numeral string to a non-negative integer.

        Examples:
            >>> Kinya._from_numeral('\ue1a0')
            0
            >>> Kinya._from_numeral('\ue1a1')
            1
            >>> Kinya._from_numeral('\ue1a4\ue1a2')
            42
            >>> Kinya._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Kinya character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
