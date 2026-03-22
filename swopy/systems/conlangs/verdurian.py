"""Verdurian numeral system converters.

This module implements numeral systems from the Verdurian conlang (by Mark
Rosenfelder).
Currently supports:

    Verdurian   U+E260-U+E269  (Private Use Area)

Verdurian uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+E200-U+E26F.  Digits 0-9
map to U+E260-U+E269.  Numbers are written most-significant digit first
(left-to-right).  Standalone shorthand glyphs for 11 (U+E26A) and 12
(U+E26B) are accepted as input but are not emitted by positional encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE260


class Verdurian(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Verdurian
    numerals.

    - Uses Unicode Private Use Area U+E260-U+E269 (UCSUR block U+E200-U+E26F)
    - The system is positional in base 10 with 10 unique digit glyphs
    - A conlang by Mark Rosenfelder
    - Standalone shorthand glyphs for 11 (U+E26A) and 12 (U+E26B) are accepted
      as input but not emitted by encoding

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

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {
        **{chr(_ZERO + i): i for i in range(10)},
        chr(0xE26A): 11,
        chr(0xE26B): 12,
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Verdurian numerals.

        Examples:
            >>> Verdurian._to_numeral(0)
            '\ue260'
            >>> Verdurian._to_numeral(1)
            '\ue261'
            >>> Verdurian._to_numeral(42)
            '\ue264\ue262'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Verdurian numeral string to a non-negative integer.

        Standalone shorthand glyphs for 11 (U+E26A) and 12 (U+E26B) are accepted.

        Examples:
            >>> Verdurian._from_numeral('\ue260')
            0
            >>> Verdurian._from_numeral('\ue261')
            1
            >>> Verdurian._from_numeral('\ue264\ue262')
            42
            >>> Verdurian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Verdurian character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
