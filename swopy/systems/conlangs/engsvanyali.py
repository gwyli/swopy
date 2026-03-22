"""Engsvanyali numeral system converters.

This module implements numeral systems from the Engsvanyali conlang.
Currently supports:

    Engsvanyali   U+E140-U+E149  (Private Use Area)

Engsvanyali uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+E100-U+E14F.  Digits 0-9
map to U+E140-U+E149.  Numbers are written most-significant digit first
(left-to-right).  Additional standalone glyphs for 10 (U+E14A), 100
(U+E14B), 1000 (U+E14C), 10000 (U+E14D), and 1000000 (U+E14E) are present
in the block and accepted as input values; they are not emitted by positional
encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE140


class Engsvanyali(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and
    Engsvanyali numerals.

    - Uses Unicode Private Use Area U+E140-U+E149 (UCSUR block U+E100-U+E14F)
    - The system is positional in base 10 with 10 unique digit glyphs
    - Standalone glyphs for 10, 100, 1000, 10000, and 1000000 (U+E14A-U+E14E)
      are accepted as input but not emitted by encoding

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
        chr(0xE14A): 10,
        chr(0xE14B): 100,
        chr(0xE14C): 1_000,
        chr(0xE14D): 10_000,
        chr(0xE14E): 1_000_000,
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Engsvanyali numerals.

        Examples:
            >>> Engsvanyali._to_numeral(0)
            '\ue140'
            >>> Engsvanyali._to_numeral(1)
            '\ue141'
            >>> Engsvanyali._to_numeral(42)
            '\ue144\ue142'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Engsvanyali numeral string to a non-negative integer.

        Standalone large-number glyphs (U+E14A-U+E14E) are accepted as input.

        Examples:
            >>> Engsvanyali._from_numeral('\ue140')
            0
            >>> Engsvanyali._from_numeral('\ue141')
            1
            >>> Engsvanyali._from_numeral('\ue144\ue142')
            42
            >>> Engsvanyali._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Engsvanyali character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
