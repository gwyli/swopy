"""Tengwar numeral system converters.

This module implements numeral systems from the Tengwar conlang (J.R.R.
Tolkien's script).
Currently supports:

    Tengwar   U+E070-U+E07B  (Private Use Area)

Tengwar uses a positional base-12 (duodecimal) encoding with twelve unique
digit glyphs assigned from the UCSUR Private Use Area block U+E000-U+E07F.
Digits 0-11 map to U+E070-U+E07B.  Numbers are written most-significant digit
first (left-to-right).  The glyph U+E07C is accepted as an alias for the
value 12 during decoding but is not emitted by encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE070


class Tengwar(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Tengwar
    numerals.

    - Uses Unicode Private Use Area U+E070-U+E07B (UCSUR block U+E000-U+E07F)
    - The system is positional in base 12 with 12 unique digit glyphs (0-11)
    - U+E07C is accepted as an alias for the standalone value 12 but not emitted

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

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(12)}
    _from_numeral_map: Mapping[str, int] = {
        **{chr(_ZERO + i): i for i in range(12)},
        chr(0xE07C): 12,  # standalone alias for 12
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Tengwar numerals.

        Examples:
            >>> Tengwar._to_numeral(0)
            '\ue070'
            >>> Tengwar._to_numeral(1)
            '\ue071'
            >>> Tengwar._to_numeral(42)
            '\ue073\ue076'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 12)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Tengwar numeral string to a non-negative integer.

        The glyph U+E07C is accepted as an alias for 12 during decoding.

        Examples:
            >>> Tengwar._from_numeral('\ue070')
            0
            >>> Tengwar._from_numeral('\ue071')
            1
            >>> Tengwar._from_numeral('\ue073\ue076')
            42
            >>> Tengwar._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Tengwar character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 12)
