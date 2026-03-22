"""Hebrew numeral system converters.

This module implements numeral systems from the Hebrew script family.
Currently supports:

    Hebrew  U+0590-U+05FF  (Hebrew letters as numerals; Geresh U+05F3
                             prefix for thousands 1,000-9,000)

Hebrew uses alphabetic letters as numerals (gematria / mispar): no dedicated
numeral code points exist; letters do double duty.  The system is purely
additive and written largest-to-smallest.  Values 1-400 are covered by the
22 base letters; 500-900 are formed by combining ת (400) with smaller letters.
Thousands 1,000-9,000 are expressed as a Geresh (׳, U+05F3) prefix followed
by the corresponding unit letter (e.g. ׳א = 1,000, ׳ט = 9,000).

The Gershayim punctuation mark (״, U+05F4) is a number indicator written
before the final letter of a multi-letter numeral; it carries no numeric
value and is ignored during decoding.

Traditional conventions replace י״ה (yod+he = 10+5 = 15) with ט״ו
(tet+vav = 9+6) and י״ו (yod+vav = 10+6 = 16) with ט״ז (tet+zayin = 9+7)
to avoid forming abbreviated divine names.

Both regular and final letterforms are accepted in decoding.
"""

# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import greedy_additive_to_numeral, longest_match_from_numeral

# Geresh prefix used to mark thousands
_GERESH = "\u05f3"  # ׳


class Hebrew(System[str, int]):
    """Implements bidirectional conversion between integers and Hebrew numerals.

    - Uses Unicode block U+0590-U+05FF (Hebrew letters as numerals)
    - The system is purely additive, written largest-to-smallest
    - Thousands 1,000-9,000 are expressed as Geresh (U+05F3) prefix + unit letter
    - Traditional substitutions apply: 15→ט״ו and 16→ט״ז
    - Gershayim (U+05F4) is accepted in decoding but carries no value
    - Both regular and final letterforms are accepted

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
        9000: "\u05f3\u05d8",  # ׳ט  nine-thousand
        8000: "\u05f3\u05d7",  # ׳ח  eight-thousand
        7000: "\u05f3\u05d6",  # ׳ז  seven-thousand
        6000: "\u05f3\u05d5",  # ׳ו  six-thousand
        5000: "\u05f3\u05d4",  # ׳ה  five-thousand
        4000: "\u05f3\u05d3",  # ׳ד  four-thousand
        3000: "\u05f3\u05d2",  # ׳ג  three-thousand
        2000: "\u05f3\u05d1",  # ׳ב  two-thousand
        1000: "\u05f3\u05d0",  # ׳א  one-thousand
        400: "\u05ea",  # ת  tav
        300: "\u05e9",  # ש  shin
        200: "\u05e8",  # ר  resh
        100: "\u05e7",  # ק  kuf
        90: "\u05e6",  # צ  tsadi
        80: "\u05e4",  # פ  pe
        70: "\u05e2",  # ע  ayin
        60: "\u05e1",  # ס  samech
        50: "\u05e0",  # נ  nun
        40: "\u05de",  # מ  mem
        30: "\u05dc",  # ל  lamed
        20: "\u05db",  # כ  kaf
        10: "\u05d9",  # י  yod
        9: "\u05d8",  # ט  tet
        8: "\u05d7",  # ח  chet
        7: "\u05d6",  # ז  zayin
        6: "\u05d5",  # ו  vav
        5: "\u05d4",  # ה  he
        4: "\u05d3",  # ד  dalet
        3: "\u05d2",  # ג  gimel
        2: "\u05d1",  # ב  bet
        1: "\u05d0",  # א  alef
    }

    # Two-char geresh+letter tokens first; single-char tokens for both
    # regular and final letterforms; Gershayim (U+05F4) maps to 0 (ignored).
    _from_numeral_map: Mapping[str, int] = {
        "\u05f3\u05d0": 1000,  # ׳א
        "\u05f3\u05d1": 2000,  # ׳ב
        "\u05f3\u05d2": 3000,  # ׳ג
        "\u05f3\u05d3": 4000,  # ׳ד
        "\u05f3\u05d4": 5000,  # ׳ה
        "\u05f3\u05d5": 6000,  # ׳ו
        "\u05f3\u05d6": 7000,  # ׳ז
        "\u05f3\u05d7": 8000,  # ׳ח
        "\u05f3\u05d8": 9000,  # ׳ט
        "\u05ea": 400,  # ת
        "\u05e9": 300,  # ש
        "\u05e8": 200,  # ר
        "\u05e7": 100,  # ק
        "\u05e6": 90,  # צ  (regular tsadi)
        "\u05e5": 90,  # ץ  (final tsadi)
        "\u05e4": 80,  # פ  (regular pe)
        "\u05e3": 80,  # ף  (final pe)
        "\u05e2": 70,  # ע
        "\u05e1": 60,  # ס
        "\u05e0": 50,  # נ  (regular nun)
        "\u05df": 50,  # ן  (final nun)
        "\u05de": 40,  # מ  (regular mem)
        "\u05dd": 40,  # ם  (final mem)
        "\u05dc": 30,  # ל
        "\u05db": 20,  # כ  (regular kaf)
        "\u05da": 20,  # ך  (final kaf)
        "\u05d9": 10,  # י
        "\u05d8": 9,  # ט
        "\u05d7": 8,  # ח
        "\u05d6": 7,  # ז
        "\u05d5": 6,  # ו
        "\u05d4": 5,  # ה
        "\u05d3": 4,  # ד
        "\u05d2": 3,  # ג
        "\u05d1": 2,  # ב
        "\u05d0": 1,  # א
        "\u05f4": 0,  # ״  gershayim (punctuation, ignored)
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Hebrew numerals.

        Uses greedy additive decomposition, then applies the traditional
        substitutions 15 → ט״ו (9+6) and 16 → ט״ז (9+7) to avoid forming
        abbreviated divine names.

        Examples:
            >>> Hebrew._to_numeral(1)
            'א'
            >>> Hebrew._to_numeral(10)
            'י'
            >>> Hebrew._to_numeral(15)
            'טו'
            >>> Hebrew._to_numeral(16)
            'טז'
            >>> Hebrew._to_numeral(100)
            'ק'
            >>> Hebrew._to_numeral(400)
            'ת'
            >>> Hebrew._to_numeral(1000)
            '׳א'
            >>> Hebrew._to_numeral(5784)
            '׳התשפד'
        """
        result = greedy_additive_to_numeral(denotation, cls._to_numeral_items)
        # Traditional substitutions to avoid abbreviated divine names
        result = result.replace(
            "\u05d9\u05d4",
            "\u05d8\u05d5",  # יה → טו  (15)
        )
        result = result.replace(
            "\u05d9\u05d5",
            "\u05d8\u05d6",  # יו → טז  (16)
        )
        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Hebrew numeral to an integer.

        Sums the values of all tokens.  Two-character Geresh+letter tokens
        (thousands) are resolved before single-character tokens.  The
        Gershayim punctuation mark (U+05F4) is consumed but contributes 0.
        Both regular and final letterforms are accepted.

        Examples:
            >>> Hebrew._from_numeral('א')
            1
            >>> Hebrew._from_numeral('י')
            10
            >>> Hebrew._from_numeral('טו')
            15
            >>> Hebrew._from_numeral('טז')
            16
            >>> Hebrew._from_numeral('ק')
            100
            >>> Hebrew._from_numeral('ת')
            400
            >>> Hebrew._from_numeral('׳א')
            1000
            >>> Hebrew._from_numeral('׳התשפד')
            5784
            >>> Hebrew._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Hebrew character at position 0: '?'
        """
        return longest_match_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
