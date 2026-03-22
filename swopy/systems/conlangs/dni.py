"""D'ni numeral system converters.

This module implements numeral systems from the D'ni conlang (from the
Myst/D'ni universe by Cyan Worlds).
Currently supports:

    Dni   U+E860-U+E878  (Private Use Area)

D'ni uses a positional base-25 encoding with twenty-five unique digit glyphs
assigned from the UCSUR Private Use Area block U+E830-U+E88F.  Digits 0-24
map to U+E860-U+E878.  Numbers are written most-significant digit first
(left-to-right).  The glyph U+E879 is accepted as a standalone alias for 25
during decoding but is not emitted by encoding.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ...system import Encodings, System
from .._algorithms import positional_from_numeral, positional_to_numeral

_ZERO = 0xE860


class Dni(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and Dni
    numerals.

    - Uses Unicode Private Use Area U+E860-U+E878 (UCSUR block U+E830-U+E88F)
    - The system is positional in base 25 with 25 unique digit glyphs (0-24)
    - From the Myst/D'ni universe by Cyan Worlds
    - U+E879 is accepted as a standalone alias for 25 but not emitted

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

    _to_numeral_map: Mapping[int, str] = {i: chr(_ZERO + i) for i in range(25)}
    _from_numeral_map: Mapping[str, int] = {
        **{chr(_ZERO + i): i for i in range(25)},
        chr(0xE879): 25,  # standalone alias for 25
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Dni numerals.

        Examples:
            >>> Dni._to_numeral(0)
            '\ue860'
            >>> Dni._to_numeral(1)
            '\ue861'
            >>> Dni._to_numeral(42)
            '\ue861\ue871'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 25)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Dni numeral string to a non-negative integer.

        The glyph U+E879 is accepted as a standalone alias for 25.

        Examples:
            >>> Dni._from_numeral('\ue860')
            0
            >>> Dni._from_numeral('\ue861')
            1
            >>> Dni._from_numeral('\ue861\ue871')
            42
            >>> Dni._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Dni character: '?'
        """
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 25)
