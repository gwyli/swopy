"""Syrrin numeral system converters.

This module implements numeral systems from the Syrrin conlang.
Currently supports:

    Syrrin   U+EC68-U+EC6D  (Private Use Area)

Syrrin uses a positional base-6 encoding with six unique digit glyphs
assigned from the UCSUR Private Use Area block U+EC30-U+EC6F.  Digits 0-5
map to U+EC68-U+EC6D.  Numbers are written most-significant digit first
(left-to-right).  The glyph U+EC6E is accepted as a standalone alias for 30
during decoding but is not emitted by encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xEC68


class Syrrin(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Syrrin
    numerals.

    - Uses Unicode Private Use Area U+EC68-U+EC6D (UCSUR block U+EC30-U+EC6F)
    - The system is positional in base 6 with 6 unique digit glyphs (0-5)
    - U+EC6E is accepted as a standalone alias for 30 but not emitted

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

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(6)}
    _from_numeral_map: Mapping[str, int] = {
        **{chr(_ZERO + i): i for i in range(6)},
        chr(0xEC6E): 30,  # standalone alias for 30
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Syrrin numerals.

        Examples:
            >>> Syrrin._to_numeral(0)
            '\uec68'
            >>> Syrrin._to_numeral(1)
            '\uec69'
            >>> Syrrin._to_numeral(42)
            '\uec69\uec69\uec68'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 6)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Syrrin numeral string to a non-negative integer.

        The glyph U+EC6E is accepted as a standalone alias for 30.

        Examples:
            >>> Syrrin._from_numeral('\uec68')
            0
            >>> Syrrin._from_numeral('\uec69')
            1
            >>> Syrrin._from_numeral('\uec69\uec69\uec68')
            42
            >>> Syrrin._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Syrrin character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 6)
