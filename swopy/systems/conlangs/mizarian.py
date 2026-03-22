"""Mizarian numeral system converters.

This module implements numeral systems from the Mizarian conlang (a Zompist
Bulletin Board conlang).
Currently supports:

    Mizarian   U+E314-U+E320  (Private Use Area)

Mizarian is a purely additive system with no zero glyph.  Encoding uses
greedy decomposition (largest denomination first); decoding sums character
values.  The system includes a subtractive glyph (-1, U+E31D) that is
accepted during decoding (e.g. 12 + (-1) = 11) but is never emitted by
greedy encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Mizarian(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Mizarian
    numerals.

    - Uses Unicode Private Use Area U+E314-U+E320 (UCSUR block U+E300-U+E33F)
    - The system is purely additive with dedicated glyphs for 1, 2, 3, 4, 5,
      6, 7, 8, 9, 12, 144, and 512
    - No zero glyph exists; minimum valid value is 1
    - A subtractive glyph (-1, U+E31D) is accepted during decoding but not emitted

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False - no upper bound exists
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        512: chr(0xE320),
        144: chr(0xE31F),
        12: chr(0xE31E),
        9: chr(0xE31C),
        8: chr(0xE31B),
        7: chr(0xE31A),
        6: chr(0xE319),
        5: chr(0xE318),
        4: chr(0xE317),
        3: chr(0xE316),
        2: chr(0xE315),
        1: chr(0xE314),
    }

    _from_numeral_map: Mapping[str, int] = {
        **{v: k for k, v in _to_numeral_map.items()},
        chr(0xE31D): -1,  # subtractive glyph
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a positive integer to Mizarian numerals.

        Examples:
            >>> Mizarian._to_numeral(1)
            '\ue314'
            >>> Mizarian._to_numeral(12)
            '\ue31e'
            >>> Mizarian._to_numeral(42)
            '\ue31e\ue31e\ue31e\ue319'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Mizarian numeral string to a positive integer.

        The subtractive glyph (U+E31D, value -1) is accepted during decoding.

        Examples:
            >>> Mizarian._from_numeral('\ue314')
            1
            >>> Mizarian._from_numeral('\ue31e')
            12
            >>> Mizarian._from_numeral('\ue31e\ue31d')
            11
            >>> Mizarian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Mizarian character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
