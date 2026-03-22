"""Cuneiform numeral system converters.

This module implements numeral systems from the Cuneiform script family.
Currently supports:

    Cuneiform   U+12400-U+1247F  (Cuneiform Numbers and Punctuation block)
                U+12000-U+123FF  (main block; ASH and DISH base signs)
    OldPersian  U+103D0-U+103D5  (Old Persian block)

Cuneiform is a purely additive system using greedy decomposition for encoding
and character-sum for decoding.  Multiple-of-10 signs (THREE DISH through
NINE DISH) and unit signs (TWO ASH through NINE ASH) are combined greedily;
the value 20 is represented by two DISH signs.

Old Persian uses five additive glyphs (1, 2, 10, 20, 100); encoding uses
greedy decomposition left-to-right and decoding sums each character.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Cuneiform(System[str, int | Fraction]):
    """Implements bidirectional conversion between integers or fractions and Cuneiform
    numerals.

    - Uses Unicode blocks U+12400-U+1247F (Numbers and Punctuation) and
      U+12000-U+123FF (main block)
    - The system is purely additive, with pre-composed signs for units
      (TWO ASH-NINE ASH) and multiples of 10 (THREE DISH-NINE DISH)
    - Value 20 is represented by two DISH signs; the base ASH (1) and DISH (10)
      come from the main block
    - Fraction signs: DISH-based thirds (1/3 at U+1245A, 2/3 at U+1245B); variant
      forms U+1245D (1/3) and U+1245E (2/3) are accepted as input but not produced
      on output; ASH-based and Old Assyrian fraction signs use incompatible
      denominators and are not supported

    Attributes:
        minimum: Minimum valid value (1/3)
        maximum: Maximum valid value (999)
        maximum_is_many: False - integers greater than 999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 3)
    maximum: ClassVar[int | float | Fraction] = 999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int | Fraction, str] = {
        90: "\U0001240e",  # 𒐎 CUNEIFORM NUMERIC SIGN NINE DISH
        80: "\U0001240d",  # 𒐍 CUNEIFORM NUMERIC SIGN EIGHT DISH
        70: "\U0001240c",  # 𒐌 CUNEIFORM NUMERIC SIGN SEVEN DISH
        60: "\U0001240b",  # 𒐋 CUNEIFORM NUMERIC SIGN SIX DISH
        50: "\U0001240a",  # 𒐊 CUNEIFORM NUMERIC SIGN FIVE DISH
        40: "\U00012409",  # 𒐉 CUNEIFORM NUMERIC SIGN FOUR DISH
        30: "\U00012408",  # 𒐈 CUNEIFORM NUMERIC SIGN THREE DISH
        10: "\U00012079",  # 𒁹 CUNEIFORM SIGN DISH (ONE DISH = 10)
        9: "\U00012407",  # 𒐇 CUNEIFORM NUMERIC SIGN NINE ASH
        8: "\U00012406",  # 𒐆 CUNEIFORM NUMERIC SIGN EIGHT ASH
        7: "\U00012405",  # 𒐅 CUNEIFORM NUMERIC SIGN SEVEN ASH
        6: "\U00012404",  # 𒐄 CUNEIFORM NUMERIC SIGN SIX ASH
        5: "\U00012403",  # 𒐃 CUNEIFORM NUMERIC SIGN FIVE ASH
        4: "\U00012402",  # 𒐂 CUNEIFORM NUMERIC SIGN FOUR ASH
        3: "\U00012401",  # 𒐁 CUNEIFORM NUMERIC SIGN THREE ASH
        2: "\U00012400",  # 𒐀 CUNEIFORM NUMERIC SIGN TWO ASH
        1: "\U00012038",  # 𒀸 CUNEIFORM SIGN ASH (ONE ASH = 1)
        Fraction(2, 3): "\U0001245b",  # 𒑛 CUNEIFORM NUMERIC SIGN TWO THIRDS DISH
        Fraction(1, 3): "\U0001245a",  # 𒑚 CUNEIFORM NUMERIC SIGN ONE THIRD DISH
    }

    _from_numeral_map: Mapping[str, int | Fraction] = {
        **{v: k for k, v in _to_numeral_map.items()},
        "\U0001245d": Fraction(1, 3),  # 𒑝 ONE THIRD DISH VARIANT FORM A
        "\U0001245e": Fraction(2, 3),  # 𒑞 TWO THIRDS DISH VARIANT FORM A
    }

    @classmethod
    def _to_numeral(cls, denotation: int | Fraction) -> str:
        """Convert an integer or fraction to Cuneiform numerals.

        The integer part uses greedy additive decomposition, largest denomination first.
        The fractional part (if any) is looked up directly in the map; only the
        discrete fraction values with dedicated glyphs are representable.

        Examples:
            >>> Cuneiform._to_numeral(1)
            '𒀸'
            >>> Cuneiform._to_numeral(9)
            '𒐇'
            >>> Cuneiform._to_numeral(10)
            '𒁹'
            >>> Cuneiform._to_numeral(15)
            '𒁹𒐃'
            >>> Cuneiform._to_numeral(31)
            '𒐈𒀸'
            >>> Cuneiform._to_numeral(99)
            '𒐎𒐇'
            >>> from fractions import Fraction
            >>> Cuneiform._to_numeral(Fraction(1, 3))
            '𒑚'
            >>> Cuneiform._to_numeral(Fraction(1, 3) + 5)
            '𒐃𒑚'
            >>> Cuneiform._to_numeral(Fraction(3, 4))
            Traceback (most recent call last):
                ...
            ValueError: 3/4 cannot be represented in Cuneiform.
        """
        if isinstance(denotation, int):
            return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

        frac = Fraction(denotation)
        integer_part = int(frac)
        frac_part = frac - integer_part

        result = greedy_additive_to_numeral(integer_part, cls._to_numeral_items)

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
        """Convert a Cuneiform numeral to an integer or fraction.

        Sums the values of each glyph in the string.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Cuneiform._from_numeral('𒀸')
            1
            >>> Cuneiform._from_numeral('𒁹𒐃')
            15
            >>> Cuneiform._from_numeral('𒐈𒀸')
            31
            >>> Cuneiform._from_numeral('𒐎𒐇')
            99
            >>> Cuneiform._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Cuneiform character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class OldPersian(System[str, int]):
    """Implements bidirectional conversion between integers and Old Persian numerals.

    - Uses Unicode block U+103D0-U+103D5 (five glyphs: 1, 2, 10, 20, 100)
    - The system is purely additive with greedy decomposition left-to-right
    - Encoding uses the largest denomination first; decoding sums each character

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (999)
        maximum_is_many: False - integers greater than 999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        100: "\U000103d5",  # 𐏕 OLD PERSIAN NUMBER HUNDRED
        20: "\U000103d4",  # 𐏔 OLD PERSIAN NUMBER TWENTY
        10: "\U000103d3",  # 𐏓 OLD PERSIAN NUMBER TEN
        2: "\U000103d2",  # 𐏒 OLD PERSIAN NUMBER TWO
        1: "\U000103d1",  # 𐏑 OLD PERSIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Old Persian numerals.

        Uses greedy additive decomposition, largest denomination first.

        Examples:
            >>> OldPersian._to_numeral(1)
            '𐏑'
            >>> OldPersian._to_numeral(2)
            '𐏒'
            >>> OldPersian._to_numeral(10)
            '𐏓'
            >>> OldPersian._to_numeral(20)
            '𐏔'
            >>> OldPersian._to_numeral(21)
            '𐏔𐏑'
            >>> OldPersian._to_numeral(100)
            '𐏕'
            >>> OldPersian._to_numeral(122)
            '𐏕𐏔𐏒'
            >>> OldPersian._to_numeral(999)
            '𐏕𐏕𐏕𐏕𐏕𐏕𐏕𐏕𐏕𐏔𐏔𐏔𐏔𐏓𐏒𐏒𐏒𐏒𐏑'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Old Persian numeral to an integer.

        Sums the values of each glyph in the string.

        Examples:
            >>> OldPersian._from_numeral('𐏑')
            1
            >>> OldPersian._from_numeral('𐏒')
            2
            >>> OldPersian._from_numeral('𐏓')
            10
            >>> OldPersian._from_numeral('𐏔')
            20
            >>> OldPersian._from_numeral('𐏕')
            100
            >>> OldPersian._from_numeral('𐏕𐏔𐏒')
            122
            >>> OldPersian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid OldPersian character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
