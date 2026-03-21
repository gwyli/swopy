"""Kharosthi numeral system converters.

This module implements numeral systems from the Kharosthi script family.
Currently supports:

    Kharosthi  U+10A40-U+10A47  (eight glyphs: units 1–4, ten, twenty,
                                  hundred, thousand)

Kharosthi is a multiplicative-additive system: unit symbols (1–4) preceding a
hundreds or thousands symbol act as a multiplier for that symbol (omitted when
1).  Tens are written additively using 20s then an optional 10; units use
greedy decomposition with 4, 3, 2, 1.  The most significant group appears
first (leftmost).
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
)


def _make_units_table(m: Mapping[int, str]) -> tuple[str, ...]:
    """Pre-compute the greedy (4,3,2,1) decomposition for all integers 0–9."""
    table: list[str] = []
    for n in range(10):
        s = ""
        rem = n
        for v in (4, 3, 2, 1):
            s += m[v] * (rem // v)
            rem %= v
        table.append(s)
    return tuple(table)


class Kharosthi(System[str, int]):
    """Kharosthi numeral system converter.

    Implements bidirectional conversion between integers and Kharosthi numeral
    strings. Kharosthi is a multiplicative-additive system: unit symbols (1–4)
    preceding a hundreds or thousands symbol act as a multiplier for that
    symbol. Tens and units are written additively. The most significant group
    appears first (leftmost) in the stored string.

    Eight distinct Unicode symbols are used:

        𐩀  U+10A40  KHAROSHTHI DIGIT ONE          ->  1
        𐩁  U+10A41  KHAROSHTHI DIGIT TWO          ->  2
        𐩂  U+10A42  KHAROSHTHI DIGIT THREE        ->  3
        𐩃  U+10A43  KHAROSHTHI DIGIT FOUR         ->  4
        𐩄  U+10A44  KHAROSHTHI NUMBER TEN         ->  10
        𐩅  U+10A45  KHAROSHTHI NUMBER TWENTY      ->  20
        𐩆  U+10A46  KHAROSHTHI NUMBER ONE HUNDRED ->  100
        𐩇  U+10A47  KHAROSHTHI NUMBER ONE THOUSAND->  1000

    The structure of a numeral is (each group optional):

        [units_multiplier] 𐩇   — thousands (multiplier omitted when 1)
        [units_multiplier] 𐩆   — hundreds  (multiplier omitted when 1)
        𐩅* 𐩄?                  — tens (additive 20s then optional 10)
        units*                 — ones (additive 4, 3, 2, 1)

    Examples:
        900  ->  𐩃𐩃𐩀𐩆  (nine × 100, where nine = 4+4+1)
        1996 ->  𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁

    Attributes:
        _to_numeral_map: Mapping of the eight base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Kharosthi glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00010a47",  # 𐩇
        100: "\U00010a46",  # 𐩆
        20: "\U00010a45",  # 𐩅
        10: "\U00010a44",  # 𐩄
        4: "\U00010a43",  # 𐩃
        3: "\U00010a42",  # 𐩂
        2: "\U00010a41",  # 𐩁
        1: "\U00010a40",  # 𐩀
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}
    _units_table: ClassVar[tuple[str, ...]] = _make_units_table(_to_numeral_map)

    @classmethod
    def _units_str(cls, n: int) -> str:
        """Express an integer 1–9 as a string of unit glyphs (4, 3, 2, 1).

        Args:
            n: An integer in the range 1–9.

        Returns:
            The greedy representation of ``n`` using unit glyphs.

        Examples:
            >>> Kharosthi._units_str(1)
            '𐩀'
            >>> Kharosthi._units_str(6)
            '𐩃𐩁'
            >>> Kharosthi._units_str(9)
            '𐩃𐩃𐩀'
        """
        return cls._units_table[n]

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Kharosthi numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted if 1) followed by the group symbol. Tens are written as
        additive 20s then an optional 10. Ones are written as additive unit
        symbols using greedy decomposition with 4, 3, 2, 1.

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The Kharosthi string representation of ``denotation``.

        Raises:
            ValueError: If ``denotation`` is outside the valid range.

        Examples:
            >>> Kharosthi._to_numeral(1)
            '𐩀'
            >>> Kharosthi._to_numeral(9)
            '𐩃𐩃𐩀'
            >>> Kharosthi._to_numeral(10)
            '𐩄'
            >>> Kharosthi._to_numeral(100)
            '𐩆'
            >>> Kharosthi._to_numeral(200)
            '𐩁𐩆'
            >>> Kharosthi._to_numeral(900)
            '𐩃𐩃𐩀𐩆'
            >>> Kharosthi._to_numeral(1000)
            '𐩇'
            >>> Kharosthi._to_numeral(1996)
            '𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁'
            >>> Kharosthi._to_numeral(9999)
            '𐩃𐩃𐩀𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩃𐩀'
        """
        result = ""

        # Thousands group: unit multiplier (omitted if 1) + 𐩇
        thousands = denotation // 1000
        denotation = denotation % 1000
        if thousands:
            if thousands > 1:
                result += cls._units_str(thousands)
            result += cls._to_numeral_map[1000]

        # Hundreds group: unit multiplier (omitted if 1) + 𐩆
        hundreds = denotation // 100
        denotation = denotation % 100
        if hundreds:
            if hundreds > 1:
                result += cls._units_str(hundreds)
            result += cls._to_numeral_map[100]

        # Tens: additive 20s then optional 10
        twenties = denotation // 20
        denotation = denotation % 20
        result += cls._to_numeral_map[20] * twenties
        tens = denotation // 10
        denotation = denotation % 10
        result += cls._to_numeral_map[10] * tens

        # Ones: additive 4, 3, 2, 1
        result += cls._units_str(denotation)

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Kharosthi numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𐩀–𐩃) accumulate in a buffer.
        When a hundreds (𐩆) or thousands (𐩇) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty); 20 (𐩅) and 10
        (𐩄) symbols are added directly and flush the unit buffer as additive
        ones first. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Kharosthi numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Kharosthi._from_numeral('𐩃𐩃𐩀')
            9
            >>> Kharosthi._from_numeral('𐩃𐩃𐩀𐩆')
            900
            >>> Kharosthi._from_numeral('𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
