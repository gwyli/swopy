"""Brahmi numeral system converters.

This module implements numeral systems from the Brahmi script family.
Currently supports:

    Brahmi  U+11052-U+11065  (twenty glyphs: units 1-9, decades 10-90,
                               hundred, thousand)

Brahmi is a multiplicative-additive system: unit symbols (1-9) preceding a
hundreds or thousands symbol act as a multiplier (omitted when 1); each
decade (10-90) has its own distinct symbol; ones are written directly.  The
most significant group appears first (leftmost).
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
)


class Brahmi(System[str, int]):
    """Implements bidirectional conversion between integers and Brahmi numerals.

    - Uses Unicode block U+11052-U+11065 (twenty glyphs: units 1-9, decades 10-90,
      hundred 𑁤, thousand 𑁥)
    - The system is multiplicative-additive: unit symbols (1-9) preceding a hundreds or
      thousands symbol act as a multiplier (omitted when 1); each decade (10-90) has its
      own distinct symbol; the most significant group appears first (leftmost)

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (9999)
        maximum_is_many: False - integers greater than 9999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00011065",  # 𑁥
        100: "\U00011064",  # 𑁤
        90: "\U00011063",  # 𑁣
        80: "\U00011062",  # 𑁢
        70: "\U00011061",  # 𑁡
        60: "\U00011060",  # 𑁠
        50: "\U0001105f",  # 𑁟
        40: "\U0001105e",  # 𑁞
        30: "\U0001105d",  # 𑁝
        20: "\U0001105c",  # 𑁜
        10: "\U0001105b",  # 𑁛
        9: "\U0001105a",  # 𑁚
        8: "\U00011059",  # 𑁙
        7: "\U00011058",  # 𑁘
        6: "\U00011057",  # 𑁗
        5: "\U00011056",  # 𑁖
        4: "\U00011055",  # 𑁕
        3: "\U00011054",  # 𑁔
        2: "\U00011053",  # 𑁓
        1: "\U00011052",  # 𑁒
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Brahmi numerals.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10-90). Ones use a dedicated unit symbol (1-9).

        Examples:
            >>> Brahmi._to_numeral(1)
            '𑁒'
            >>> Brahmi._to_numeral(9)
            '𑁚'
            >>> Brahmi._to_numeral(10)
            '𑁛'
            >>> Brahmi._to_numeral(11)
            '𑁛𑁒'
            >>> Brahmi._to_numeral(99)
            '𑁣𑁚'
            >>> Brahmi._to_numeral(100)
            '𑁤'
            >>> Brahmi._to_numeral(200)
            '𑁓𑁤'
            >>> Brahmi._to_numeral(999)
            '𑁚𑁤𑁣𑁚'
            >>> Brahmi._to_numeral(1000)
            '𑁥'
            >>> Brahmi._to_numeral(1996)
            '𑁥𑁚𑁤𑁣𑁗'
            >>> Brahmi._to_numeral(9999)
            '𑁚𑁥𑁚𑁤𑁣𑁚'
        """
        return multiplicative_additive_to_numeral(denotation, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Brahmi numeral to an integer.

        Scans left-to-right. Unit symbols (𑁒-𑁚) accumulate in a buffer.
        When a hundreds (𑁤) or thousands (𑁥) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑁛-𑁣) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Examples:
            >>> Brahmi._from_numeral('𑁚')
            9
            >>> Brahmi._from_numeral('𑁚𑁤𑁣𑁚')
            999
            >>> Brahmi._from_numeral('𑁥𑁚𑁤𑁣𑁗')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
