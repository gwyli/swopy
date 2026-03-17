"""Brahmi numeral system converters.

This module implements numeral systems from the Brahmi script family.
Currently supports:

    Brahmi  U+11052-U+11065  (twenty glyphs: units 1–9, decades 10–90,
                               hundred, thousand)

Brahmi is a multiplicative-additive system: unit symbols (1–9) preceding a
hundreds or thousands symbol act as a multiplier (omitted when 1); each
decade (10–90) has its own distinct symbol; ones are written directly.  The
most significant group appears first (leftmost).
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
)


class Brahmi(System[str, int]):
    """Brahmi numeral system converter.

    Implements bidirectional conversion between integers and Brahmi numeral
    strings. Brahmi is a multiplicative-additive system: unit symbols (1–9)
    preceding a hundreds or thousands symbol act as a multiplier (omitted
    when 1); each decade (10–90) has its own distinct symbol; ones are
    written directly. The most significant group appears first (leftmost).

    Twenty distinct Unicode symbols are used:

        𑁒  U+11052  BRAHMI NUMBER ONE          ->  1
        𑁓  U+11053  BRAHMI NUMBER TWO          ->  2
        𑁔  U+11054  BRAHMI NUMBER THREE        ->  3
        𑁕  U+11055  BRAHMI NUMBER FOUR         ->  4
        𑁖  U+11056  BRAHMI NUMBER FIVE         ->  5
        𑁗  U+11057  BRAHMI NUMBER SIX          ->  6
        𑁘  U+11058  BRAHMI NUMBER SEVEN        ->  7
        𑁙  U+11059  BRAHMI NUMBER EIGHT        ->  8
        𑁚  U+1105A  BRAHMI NUMBER NINE         ->  9
        𑁛  U+1105B  BRAHMI NUMBER TEN          ->  10
        𑁜  U+1105C  BRAHMI NUMBER TWENTY       ->  20
        𑁝  U+1105D  BRAHMI NUMBER THIRTY       ->  30
        𑁞  U+1105E  BRAHMI NUMBER FORTY        ->  40
        𑁟  U+1105F  BRAHMI NUMBER FIFTY        ->  50
        𑁠  U+11060  BRAHMI NUMBER SIXTY        ->  60
        𑁡  U+11061  BRAHMI NUMBER SEVENTY      ->  70
        𑁢  U+11062  BRAHMI NUMBER EIGHTY       ->  80
        𑁣  U+11063  BRAHMI NUMBER NINETY       ->  90
        𑁤  U+11064  BRAHMI NUMBER ONE HUNDRED  ->  100
        𑁥  U+11065  BRAHMI NUMBER ONE THOUSAND ->  1000

    The structure of a numeral is (each group optional):

        [unit_multiplier] 𑁥  — thousands (multiplier omitted when 1)
        [unit_multiplier] 𑁤  — hundreds  (multiplier omitted when 1)
        decade_symbol?        — one of 𑁛–𑁣 (10, 20, …, 90)
        unit_symbol?          — one of 𑁒–𑁚 (1–9)

    Examples:
        200  ->  𑁓𑁤  (two × 100)
        999  ->  𑁚𑁤𑁣𑁚  (nine × 100, ninety, nine)
        1996 ->  𑁥𑁚𑁤𑁣𑁗

    Attributes:
        _to_numeral_map: Mapping of the twenty base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Brahmi glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

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
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Brahmi numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10–90). Ones use a dedicated unit symbol (1–9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The Brahmi string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

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
        return multiplicative_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Brahmi numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𑁒–𑁚) accumulate in a buffer.
        When a hundreds (𑁤) or thousands (𑁥) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑁛–𑁣) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Brahmi numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

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
