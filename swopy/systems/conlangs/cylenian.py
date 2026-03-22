"""Cylenian numeral system converters.

This module implements numeral systems from the Cylenian conlang.
Currently supports:

    Cylenian   U+EC28-U+EC2D  (Private Use Area)

Cylenian uses a positional base-6 encoding with six unique digit glyphs
assigned from the UCSUR Private Use Area block U+EC00-U+EC2F.  Digits 0-5
map to U+EC28-U+EC2D.  Numbers are written most-significant digit first
(left-to-right).  The glyph U+EC2E is accepted as a standalone alias for 30
during decoding but is not emitted by encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xEC28


class Cylenian(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Cylenian
    numerals.

    - Uses Unicode Private Use Area U+EC28-U+EC2D (UCSUR block U+EC00-U+EC2F)
    - The system is positional in base 6 with 6 unique digit glyphs (0-5)
    - U+EC2E is accepted as a standalone alias for 30 but not emitted

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
        chr(0xEC2E): 30,  # standalone alias for 30
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Cylenian numerals.

        Examples:
            >>> Cylenian._to_numeral(0)
            '\uec28'
            >>> Cylenian._to_numeral(1)
            '\uec29'
            >>> Cylenian._to_numeral(42)
            '\uec29\uec29\uec28'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 6)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Cylenian numeral string to a non-negative integer.

        The glyph U+EC2E is accepted as a standalone alias for 30.

        Examples:
            >>> Cylenian._from_numeral('\uec28')
            0
            >>> Cylenian._from_numeral('\uec29')
            1
            >>> Cylenian._from_numeral('\uec29\uec29\uec28')
            42
            >>> Cylenian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Cylenian character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 6)
