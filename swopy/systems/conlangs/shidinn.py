"""Shidinn numeral system converters.

This module implements numeral systems from the Shidinn conlang.
Currently supports:

    Shidinn   U+F1C20-U+F1C29  (Private Use Area)

Shidinn uses a positional base-10 encoding with ten unique digit glyphs
assigned from the UCSUR Private Use Area block U+F1B00-U+F1C3F.  Each digit
position is a power of 10; numbers are written most-significant digit first
(left-to-right).  The codepoint U+F1C2A (SIGNIFICANT ZERO) is accepted as
an alternative form of zero during decoding but is not emitted by encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral


class Shidinn(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Shidinn
    numerals.

    - Uses Unicode Private Use Area U+F1C20-U+F1C29 (UCSUR block U+F1B00-U+F1C3F)
    - The system is positional in base 10 with 10 unique digit glyphs
    - U+F1C2A (SIGNIFICANT ZERO) is accepted as input for zero but not emitted

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

    _to_numeral_map: Mapping[int, str] = {i: chr(0xF1C20 + i) for i in range(10)}
    _from_numeral_map: Mapping[str, int] = {
        **{chr(0xF1C20 + i): i for i in range(10)},
        chr(0xF1C2A): 0,  # SIGNIFICANT ZERO
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Shidinn numerals.

        Examples:
            >>> Shidinn._to_numeral(0)
            '\U000f1c20'
            >>> Shidinn._to_numeral(1)
            '\U000f1c21'
            >>> Shidinn._to_numeral(42)
            '\U000f1c24\U000f1c22'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Shidinn numeral string to a non-negative integer.

        The SIGNIFICANT ZERO glyph (U+F1C2A) is accepted as an alias for zero.

        Examples:
            >>> Shidinn._from_numeral('\U000f1c20')
            0
            >>> Shidinn._from_numeral('\U000f1c21')
            1
            >>> Shidinn._from_numeral('\U000f1c24\U000f1c22')
            42
            >>> Shidinn._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Shidinn character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)
