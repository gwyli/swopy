"""Meroitic numeral system converters.

This module implements numeral systems from the Meroitic script family.
Currently supports:

    MeroiticCursive  U+109A0-U+109FF

Meroitic Cursive is a purely additive system written right-to-left (largest
denomination on the right).  Integers use greedy decomposition followed by
reversal; the values 80 and 90 have no dedicated glyphs and are encoded as
70+10 and 70+20 respectively.  Fractions (twelfths) are appended after the
reversed integer string.  Decoding reverses the input before summing integer
glyphs; fraction glyphs are identified separately.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class MeroiticCursive(System[str, int | Fraction]):
    """Implements bidirectional conversion between integers or fractions and
    Meroitic Cursive numerals.

    - Uses Unicode block U+109A0-U+109FF (70 integer glyphs covering 1-9, 10-70,
      100-900, 1000-9000, 10000-90000, 100000-900000; and 11 fraction glyphs
      covering all twelfths from 1/12 to 11/12)
    - The system is purely additive and written right-to-left (largest denomination
      on the right); 80 and 90 have no dedicated glyphs
    - Fractions are appended to the reversed integer string; U+109BD is the
      canonical 1/2 output; U+109FB (SIX TWELFTHS) is accepted as input only

    Attributes:
        minimum: Minimum valid value (1/12)
        maximum: Maximum valid value (999999)
        maximum_is_many: False - integers greater than 999999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 12)
    maximum: ClassVar[int | float | Fraction] = 999_999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int | Fraction, str] = {
        900_000: "\U000109f5",  # 𐧵 MEROITIC CURSIVE NUMBER NINE HUNDRED THOUSAND
        800_000: "\U000109f4",  # 𐧴 MEROITIC CURSIVE NUMBER EIGHT HUNDRED THOUSAND
        700_000: "\U000109f3",  # 𐧳 MEROITIC CURSIVE NUMBER SEVEN HUNDRED THOUSAND
        600_000: "\U000109f2",  # 𐧲 MEROITIC CURSIVE NUMBER SIX HUNDRED THOUSAND
        500_000: "\U000109f1",  # 𐧱 MEROITIC CURSIVE NUMBER FIVE HUNDRED THOUSAND
        400_000: "\U000109f0",  # 𐧰 MEROITIC CURSIVE NUMBER FOUR HUNDRED THOUSAND
        300_000: "\U000109ef",  # 𐧯 MEROITIC CURSIVE NUMBER THREE HUNDRED THOUSAND
        200_000: "\U000109ee",  # 𐧮 MEROITIC CURSIVE NUMBER TWO HUNDRED THOUSAND
        100_000: "\U000109ed",  # 𐧭 MEROITIC CURSIVE NUMBER ONE HUNDRED THOUSAND
        90_000: "\U000109ec",  # 𐧬 MEROITIC CURSIVE NUMBER NINETY THOUSAND
        80_000: "\U000109eb",  # 𐧫 MEROITIC CURSIVE NUMBER EIGHTY THOUSAND
        70_000: "\U000109ea",  # 𐧪 MEROITIC CURSIVE NUMBER SEVENTY THOUSAND
        60_000: "\U000109e9",  # 𐧩 MEROITIC CURSIVE NUMBER SIXTY THOUSAND
        50_000: "\U000109e8",  # 𐧨 MEROITIC CURSIVE NUMBER FIFTY THOUSAND
        40_000: "\U000109e7",  # 𐧧 MEROITIC CURSIVE NUMBER FORTY THOUSAND
        30_000: "\U000109e6",  # 𐧦 MEROITIC CURSIVE NUMBER THIRTY THOUSAND
        20_000: "\U000109e5",  # 𐧥 MEROITIC CURSIVE NUMBER TWENTY THOUSAND
        10_000: "\U000109e4",  # 𐧤 MEROITIC CURSIVE NUMBER TEN THOUSAND
        9_000: "\U000109e3",  # 𐧣 MEROITIC CURSIVE NUMBER NINE THOUSAND
        8_000: "\U000109e2",  # 𐧢 MEROITIC CURSIVE NUMBER EIGHT THOUSAND
        7_000: "\U000109e1",  # 𐧡 MEROITIC CURSIVE NUMBER SEVEN THOUSAND
        6_000: "\U000109e0",  # 𐧠 MEROITIC CURSIVE NUMBER SIX THOUSAND
        5_000: "\U000109df",  # 𐧟 MEROITIC CURSIVE NUMBER FIVE THOUSAND
        4_000: "\U000109de",  # 𐧞 MEROITIC CURSIVE NUMBER FOUR THOUSAND
        3_000: "\U000109dd",  # 𐧝 MEROITIC CURSIVE NUMBER THREE THOUSAND
        2_000: "\U000109dc",  # 𐧜 MEROITIC CURSIVE NUMBER TWO THOUSAND
        1_000: "\U000109db",  # 𐧛 MEROITIC CURSIVE NUMBER ONE THOUSAND
        900: "\U000109da",  # 𐧚 MEROITIC CURSIVE NUMBER NINE HUNDRED
        800: "\U000109d9",  # 𐧙 MEROITIC CURSIVE NUMBER EIGHT HUNDRED
        700: "\U000109d8",  # 𐧘 MEROITIC CURSIVE NUMBER SEVEN HUNDRED
        600: "\U000109d7",  # 𐧗 MEROITIC CURSIVE NUMBER SIX HUNDRED
        500: "\U000109d6",  # 𐧖 MEROITIC CURSIVE NUMBER FIVE HUNDRED
        400: "\U000109d5",  # 𐧕 MEROITIC CURSIVE NUMBER FOUR HUNDRED
        300: "\U000109d4",  # 𐧔 MEROITIC CURSIVE NUMBER THREE HUNDRED
        200: "\U000109d3",  # 𐧓 MEROITIC CURSIVE NUMBER TWO HUNDRED
        100: "\U000109d2",  # 𐧒 MEROITIC CURSIVE NUMBER ONE HUNDRED
        70: "\U000109cf",  # 𐧏 MEROITIC CURSIVE NUMBER SEVENTY
        60: "\U000109ce",  # 𐧎 MEROITIC CURSIVE NUMBER SIXTY
        50: "\U000109cd",  # 𐧍 MEROITIC CURSIVE NUMBER FIFTY
        40: "\U000109cc",  # 𐧌 MEROITIC CURSIVE NUMBER FORTY
        30: "\U000109cb",  # 𐧋 MEROITIC CURSIVE NUMBER THIRTY
        20: "\U000109ca",  # 𐧊 MEROITIC CURSIVE NUMBER TWENTY
        10: "\U000109c9",  # 𐧉 MEROITIC CURSIVE NUMBER TEN
        9: "\U000109c8",  # 𐧈 MEROITIC CURSIVE NUMBER NINE
        8: "\U000109c7",  # 𐧇 MEROITIC CURSIVE NUMBER EIGHT
        7: "\U000109c6",  # 𐧆 MEROITIC CURSIVE NUMBER SEVEN
        6: "\U000109c5",  # 𐧅 MEROITIC CURSIVE NUMBER SIX
        5: "\U000109c4",  # 𐧄 MEROITIC CURSIVE NUMBER FIVE
        4: "\U000109c3",  # 𐧃 MEROITIC CURSIVE NUMBER FOUR
        3: "\U000109c2",  # 𐧂 MEROITIC CURSIVE NUMBER THREE
        2: "\U000109c1",  # 𐧁 MEROITIC CURSIVE NUMBER TWO
        1: "\U000109c0",  # 𐧀 MEROITIC CURSIVE NUMBER ONE
        Fraction(11, 12): "\U000109bc",  # 𐦼 MEROITIC CURSIVE FRACTION ELEVEN TWELFTHS
        Fraction(1, 2): "\U000109bd",  # 𐦽 MEROITIC CURSIVE FRACTION ONE HALF
        Fraction(5, 6): "\U000109ff",  # 𐧿 MEROITIC CURSIVE FRACTION TEN TWELFTHS
        Fraction(3, 4): "\U000109fe",  # 𐧾 MEROITIC CURSIVE FRACTION NINE TWELFTHS
        Fraction(2, 3): "\U000109fd",  # 𐧽 MEROITIC CURSIVE FRACTION EIGHT TWELFTHS
        Fraction(7, 12): "\U000109fc",  # 𐧼 MEROITIC CURSIVE FRACTION SEVEN TWELFTHS
        Fraction(5, 12): "\U000109fa",  # 𐧺 MEROITIC CURSIVE FRACTION FIVE TWELFTHS
        Fraction(1, 3): "\U000109f9",  # 𐧹 MEROITIC CURSIVE FRACTION FOUR TWELFTHS
        Fraction(1, 4): "\U000109f8",  # 𐧸 MEROITIC CURSIVE FRACTION THREE TWELFTHS
        Fraction(1, 6): "\U000109f7",  # 𐧷 MEROITIC CURSIVE FRACTION TWO TWELFTHS
        Fraction(1, 12): "\U000109f6",  # 𐧶 MEROITIC CURSIVE FRACTION ONE TWELFTH
    }

    _from_numeral_map: Mapping[str, int | Fraction] = {
        **{v: k for k, v in _to_numeral_map.items()},
        "\U000109fb": Fraction(1, 2),  # 𐧻 SIX TWELFTHS (decode-only alias)
    }

    @classmethod
    def _to_numeral(cls, denotation: int | Fraction) -> str:
        """Convert an integer or fraction to Meroitic Cursive numerals.

        The integer part uses greedy additive decomposition, largest denomination first,
        then reversed for right-to-left ordering.  The fractional part (if any) is
        looked up directly in the map and appended.

        Examples:
            >>> MeroiticCursive._to_numeral(1)
            '𐧀'
            >>> MeroiticCursive._to_numeral(9)
            '𐧈'
            >>> MeroiticCursive._to_numeral(10)
            '𐧉'
            >>> MeroiticCursive._to_numeral(80)
            '𐧉𐧏'
            >>> MeroiticCursive._to_numeral(100)
            '𐧒'
            >>> MeroiticCursive._to_numeral(1000)
            '𐧛'
            >>> from fractions import Fraction
            >>> MeroiticCursive._to_numeral(Fraction(1, 12))
            '𐧶'
            >>> MeroiticCursive._to_numeral(Fraction(11, 12))
            '𐦼'
            >>> MeroiticCursive._to_numeral(Fraction(3, 2))
            '𐧀𐦽'
            >>> MeroiticCursive._to_numeral(Fraction(5, 4))
            '𐧀𐧸'
            >>> MeroiticCursive._to_numeral(Fraction(1, 5))
            Traceback (most recent call last):
                ...
            ValueError: 1/5 cannot be represented in MeroiticCursive.
        """
        if isinstance(denotation, int):
            return reversed_greedy_additive_to_numeral(
                denotation, cls._to_numeral_items
            )

        frac = Fraction(denotation)
        integer_part = int(frac)
        frac_part = frac - integer_part

        result = (
            reversed_greedy_additive_to_numeral(integer_part, cls._to_numeral_items)
            if integer_part
            else ""
        )

        if frac_part:
            frac_glyph = cls._to_numeral_map.get(frac_part)
            if frac_glyph is None:
                raise ValueError(
                    f"{denotation} cannot be represented in {cls.__name__}."
                )
            result += frac_glyph

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int | Fraction:
        """Convert a Meroitic Cursive numeral to an integer or fraction.

        Sums the values of each glyph in the string.

        Examples:
            >>> MeroiticCursive._from_numeral('𐧀')
            1
            >>> MeroiticCursive._from_numeral('𐧈')
            9
            >>> MeroiticCursive._from_numeral('𐧉')
            10
            >>> MeroiticCursive._from_numeral('𐧉𐧏')
            80
            >>> MeroiticCursive._from_numeral('𐧒')
            100
            >>> MeroiticCursive._from_numeral('𐧛')
            1000
            >>> MeroiticCursive._from_numeral('𐧶')
            Fraction(1, 12)
            >>> MeroiticCursive._from_numeral('𐦼')
            Fraction(11, 12)
            >>> MeroiticCursive._from_numeral('𐧀𐦽')
            Fraction(3, 2)
            >>> MeroiticCursive._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid MeroiticCursive character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
