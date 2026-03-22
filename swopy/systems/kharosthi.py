"""Kharosthi numeral system converters.

This module implements numeral systems from the Kharosthi script family.
Currently supports:

    Kharosthi  U+10A40-U+10A47

Kharosthi is a multiplicative-additive system: unit symbols (1-4) preceding a
hundreds or thousands symbol act as a multiplier for that symbol (omitted when
1).  Tens are written additively using 20s then an optional 10; units use
greedy decomposition with 4, 3, 2, 1.  The most significant group appears
first (leftmost).
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
)


def _make_units_table(m: Mapping[int | Fraction, str]) -> tuple[str, ...]:
    """Pre-compute the greedy (4,3,2,1) decomposition for all integers 0-9."""
    table: list[str] = []
    for n in range(10):
        s = ""
        rem = n
        for v in (4, 3, 2, 1):
            s += m[v] * (rem // v)
            rem %= v
        table.append(s)
    return tuple(table)


class Kharosthi(System[str, int | Fraction]):
    """Implements bidirectional conversion between integers or fractions and Kharosthi
    numerals.

    - Uses Unicode block U+10A40-U+10A48 (nine glyphs: ½, units 1-4, ten, twenty,
      hundred, thousand)
    - The system is multiplicative-additive: unit symbols (1-4) preceding a hundreds or
      thousands symbol act as a multiplier (omitted when 1); tens are written additively
      using 20s then an optional 10; units use greedy decomposition with 4, 3, 2, 1
    - U+10A48 KHAROSHTHI FRACTION ONE HALF is a standalone terminal glyph (½)

    Attributes:
        minimum: Minimum valid value (1/2)
        maximum: Maximum valid value (9999)
        maximum_is_many: False - integers greater than 9999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 2)
    maximum: ClassVar[int | float | Fraction] = 9999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int | Fraction, str] = {
        1000: "\U00010a47",  # 𐩇
        100: "\U00010a46",  # 𐩆
        20: "\U00010a45",  # 𐩅
        10: "\U00010a44",  # 𐩄
        4: "\U00010a43",  # 𐩃
        3: "\U00010a42",  # 𐩂
        2: "\U00010a41",  # 𐩁
        1: "\U00010a40",  # 𐩀
        Fraction(1, 2): "\U00010a48",  # 𐩈 KHAROSHTHI FRACTION ONE HALF
    }

    _from_numeral_map: Mapping[str, int | Fraction] = {
        v: k for k, v in _to_numeral_map.items()
    }
    _units_table: ClassVar[tuple[str, ...]] = _make_units_table(_to_numeral_map)

    @classmethod
    def _units_str(cls, n: int) -> str:
        """Express an integer 1-9 as a string of unit glyphs (4, 3, 2, 1).

        Args:
            n: An integer in the range 1-9.

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
    def _to_numeral(cls, denotation: int | Fraction) -> str:
        """Convert an Arabic integer or fraction to Kharosthi numerals.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted if 1) followed by the group symbol. Tens are written as
        additive 20s then an optional 10. Ones are written as additive unit
        symbols using greedy decomposition with 4, 3, 2, 1. A trailing ½ glyph
        is appended when the fractional part equals 1/2.

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
            >>> from fractions import Fraction
            >>> Kharosthi._to_numeral(Fraction(1, 2))
            '𐩈'
            >>> Kharosthi._to_numeral(Fraction(3, 2))
            '𐩀𐩈'
            >>> Kharosthi._to_numeral(Fraction(1, 3))
            Traceback (most recent call last):
                ...
            ValueError: 1/3 cannot be represented in Kharosthi.
        """
        if isinstance(denotation, int):
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

        frac = Fraction(denotation)
        integer_part = int(frac)
        frac_part = frac - integer_part

        result = cls._to_numeral(integer_part) if integer_part else ""

        if frac_part == Fraction(1, 2):
            result += cls._to_numeral_map[Fraction(1, 2)]
        elif frac_part:
            raise ValueError(f"{denotation} cannot be represented in {cls.__name__}.")

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int | Fraction:
        """Convert a Kharosthi numeral to an integer or fraction.

        Scans left-to-right. Unit symbols (𐩀-𐩃) accumulate in a buffer.
        When a hundreds (𐩆) or thousands (𐩇) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty); 20 (𐩅) and 10
        (𐩄) symbols are added directly and flush the unit buffer as additive
        ones first. Any remaining buffer is added as ones at the end.

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
