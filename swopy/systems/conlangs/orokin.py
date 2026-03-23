"""Orokin numeral system converters.

This module implements numeral systems from the Orokin conlang (Warframe universe
by Digital Extremes).
Currently supports:

    Orokin   U+EB30-U+EB39  (Private Use Area)

Orokin uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+EB00-U+EB3F.  Each digit
position is a power of 10; numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Orokin(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Orokin
    numerals.

    - Uses Unicode Private Use Area U+EB30-U+EB39 (UCSUR block U+EB00-U+EB3F)
    - The system is positional in base 10 with 10 unique digit glyphs
    - From the Warframe fictional universe by Digital Extremes

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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xEB30 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {chr(0xEB30 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Orokin numerals.

        Examples:
            >>> Orokin._to_numeral(0)
            '\ueb30'
            >>> Orokin._to_numeral(1)
            '\ueb31'
            >>> Orokin._to_numeral(42)
            '\ueb34\ueb32'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Orokin numeral string to a non-negative integer.

        Examples:
            >>> Orokin._from_numeral('\ueb30')
            0
            >>> Orokin._from_numeral('\ueb31')
            1
            >>> Orokin._from_numeral('\ueb34\ueb32')
            42
            >>> Orokin._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Orokin character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
