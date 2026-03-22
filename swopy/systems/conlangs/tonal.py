"""Tonal numeral system converters.

This module implements numeral systems from the Tonal conlang (invented by
John W. Nystrom in 1862).
Currently supports:

    Tonal   U+E8E0-U+E8FF  (Private Use Area, digits 9-15 only)

Tonal uses a positional base-16 (hexadecimal) encoding.  Digits 0-8 reuse
standard ASCII digit glyphs ('0'-'8'); digits 9-15 use UCSUR Private Use
Area glyphs U+E8E9-U+E8EF.  Numbers are written most-significant digit first
(left-to-right).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Tonal(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Tonal
    numerals.

    - Uses standard ASCII '0'-'8' for digits 0-8 and Unicode Private Use Area
      U+E8E9-U+E8EF (UCSUR block U+E8E0-U+E8FF) for digits 9-15
    - The system is positional in base 16 with 16 unique digit glyphs
    - Invented by John W. Nystrom in 1862; digit names: Noll An De Ti Go Su By
      Ra Me Ni Ko Hu Vy La Po Fy

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

    _to_numeral_map: Mapping[int, str] = {
        **{i: chr(0x30 + i) for i in range(9)},  # '0'-'8'
        **{i + 9: chr(0xE8E9 + i) for i in range(7)},  # 9-15 -> PUA
    }
    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Tonal numerals.

        Examples:
            >>> Tonal._to_numeral(0)
            '0'
            >>> Tonal._to_numeral(8)
            '8'
            >>> Tonal._to_numeral(42)
            '2\ue8ea'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 16)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Tonal numeral string to a non-negative integer.

        Examples:
            >>> Tonal._from_numeral('0')
            0
            >>> Tonal._from_numeral('8')
            8
            >>> Tonal._from_numeral('2\ue8ea')
            42
            >>> Tonal._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Tonal character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 16)
