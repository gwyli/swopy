"""Brahmi-Gupta script family numeral system converters.

This module implements numeral systems from the Brahmi-Gupta script family.
Currently supports:

    Sinhala Archaic  U+111E0-U+111FF  (twenty glyphs: units 1-9, decades 10-90,
                                        hundred, thousand; U+111E1-U+111F4)
    Bhaiksuki        U+11C00-U+11C6F  (twenty-eight glyphs: units 1-9,
                                        decades 10-90, hundreds mark U+11C6C;
                                        number signs U+11C5A-U+11C6C)

Sinhala Archaic (also known as Bakhshali) is a multiplicative-additive system
identical in structure to Brahmi: unit symbols (1-9) preceding a hundreds or
thousands symbol act as a multiplier (omitted when 1); each decade (10-90) has
its own symbol; ones are written directly.

Bhaiksuki is a multiplicative-additive system with dedicated unit signs (1-9),
decade signs (10-90), and a hundreds unit mark (U+11C6C) that follows a unit
sign to form hundreds (100-900). Encoding uses greedy decomposition; decoding
uses longest-match scanning to disambiguate two-character hundred tokens from
their constituent single-character unit signs.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    greedy_additive_to_numeral,
    longest_match_from_numeral,
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
)

# Bhaiksuki hundreds unit mark (U+11C6C); combined with unit signs to form 100-900
_BHAIKSUKI_HUNDREDS_MARK = "\U00011c6c"


class SinhalaArchaic(System[str, int]):
    """Sinhala Archaic numeral system converter.

    Implements bidirectional conversion between integers and Sinhala Archaic
    numeral strings using Unicode block U+111E0-U+111FF. The system is
    multiplicative-additive, identical in structure to Brahmi: unit symbols
    (1-9) preceding a hundreds or thousands symbol act as a multiplier
    (omitted when 1); each decade (10-90) has its own symbol; ones are written
    directly. The most significant group appears first (leftmost).

    Twenty distinct Unicode symbols are used:

        𑇡  U+111E1  SINHALA ARCHAIC DIGIT ONE          ->  1
        𑇢  U+111E2  SINHALA ARCHAIC DIGIT TWO          ->  2
        𑇣  U+111E3  SINHALA ARCHAIC DIGIT THREE        ->  3
        𑇤  U+111E4  SINHALA ARCHAIC DIGIT FOUR         ->  4
        𑇥  U+111E5  SINHALA ARCHAIC DIGIT FIVE         ->  5
        𑇦  U+111E6  SINHALA ARCHAIC DIGIT SIX          ->  6
        𑇧  U+111E7  SINHALA ARCHAIC DIGIT SEVEN        ->  7
        𑇨  U+111E8  SINHALA ARCHAIC DIGIT EIGHT        ->  8
        𑇩  U+111E9  SINHALA ARCHAIC DIGIT NINE         ->  9
        𑇪  U+111EA  SINHALA ARCHAIC NUMBER TEN         ->  10
        𑇫  U+111EB  SINHALA ARCHAIC NUMBER TWENTY      ->  20
        𑇬  U+111EC  SINHALA ARCHAIC NUMBER THIRTY      ->  30
        𑇭  U+111ED  SINHALA ARCHAIC NUMBER FORTY       ->  40
        𑇮  U+111EE  SINHALA ARCHAIC NUMBER FIFTY       ->  50
        𑇯  U+111EF  SINHALA ARCHAIC NUMBER SIXTY       ->  60
        𑇰  U+111F0  SINHALA ARCHAIC NUMBER SEVENTY     ->  70
        𑇱  U+111F1  SINHALA ARCHAIC NUMBER EIGHTY      ->  80
        𑇲  U+111F2  SINHALA ARCHAIC NUMBER NINETY      ->  90
        𑇳  U+111F3  SINHALA ARCHAIC NUMBER ONE HUNDRED ->  100
        𑇴  U+111F4  SINHALA ARCHAIC NUMBER ONE THOUSAND->  1000

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        encodings: UTF-8 only; glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U000111f4",  # 𑇴
        100: "\U000111f3",  # 𑇳
        90: "\U000111f2",  # 𑇲
        80: "\U000111f1",  # 𑇱
        70: "\U000111f0",  # 𑇰
        60: "\U000111ef",  # 𑇯
        50: "\U000111ee",  # 𑇮
        40: "\U000111ed",  # 𑇭
        30: "\U000111ec",  # 𑇬
        20: "\U000111eb",  # 𑇫
        10: "\U000111ea",  # 𑇪
        9: "\U000111e9",  # 𑇩
        8: "\U000111e8",  # 𑇨
        7: "\U000111e7",  # 𑇧
        6: "\U000111e6",  # 𑇦
        5: "\U000111e5",  # 𑇥
        4: "\U000111e4",  # 𑇤
        3: "\U000111e3",  # 𑇣
        2: "\U000111e2",  # 𑇢
        1: "\U000111e1",  # 𑇡
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Sinhala Archaic numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10-90). Ones use a dedicated unit symbol (1-9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The Sinhala Archaic string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> SinhalaArchaic._to_numeral(1)
            '𑇡'
            >>> SinhalaArchaic._to_numeral(9)
            '𑇩'
            >>> SinhalaArchaic._to_numeral(10)
            '𑇪'
            >>> SinhalaArchaic._to_numeral(11)
            '𑇪𑇡'
            >>> SinhalaArchaic._to_numeral(100)
            '𑇳'
            >>> SinhalaArchaic._to_numeral(200)
            '𑇢𑇳'
            >>> SinhalaArchaic._to_numeral(999)
            '𑇩𑇳𑇲𑇩'
            >>> SinhalaArchaic._to_numeral(1996)
            '𑇴𑇩𑇳𑇲𑇦'
        """
        return multiplicative_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Sinhala Archaic numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𑇡-𑇩) accumulate in a buffer.
        When a hundreds (𑇳) or thousands (𑇴) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑇪-𑇲) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Sinhala Archaic numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> SinhalaArchaic._from_numeral('𑇩')
            9
            >>> SinhalaArchaic._from_numeral('𑇩𑇳𑇲𑇩')
            999
            >>> SinhalaArchaic._from_numeral('𑇴𑇩𑇳𑇲𑇦')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class Bhaiksuki(System[str, int]):
    """Bhaiksuki numeral system converter.

    Implements bidirectional conversion between integers and Bhaiksuki numeral
    strings using Unicode block U+11C00-U+11C6F. The system uses dedicated
    unit signs (1-9) at U+11C5A-U+11C62, decade signs (10-90) at
    U+11C63-U+11C6B, and a hundreds unit mark (U+11C6C) that follows a unit
    sign to form hundreds (100-900). The valid range is 1-999.

    The hundreds group is encoded as a two-character sequence: the unit sign
    for the coefficient followed by the hundreds mark. Encoding uses greedy
    additive decomposition (largest denomination first); decoding uses
    longest-match scanning so that two-character hundred tokens are resolved
    before their constituent single-character unit signs.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
        encodings: UTF-8 only; glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        # Hundreds: unit-sign + hundreds-mark (two-character glyphs)
        900: "\U00011c62" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱢𑱬
        800: "\U00011c61" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱡𑱬
        700: "\U00011c60" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱠𑱬
        600: "\U00011c5f" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱟𑱬
        500: "\U00011c5e" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱞𑱬
        400: "\U00011c5d" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱝𑱬
        300: "\U00011c5c" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱜𑱬
        200: "\U00011c5b" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱛𑱬
        100: "\U00011c5a" + _BHAIKSUKI_HUNDREDS_MARK,  # 𑱚𑱬
        # Decades: single-character glyphs
        90: "\U00011c6b",  # 𑱫 BHAIKSUKI NUMBER NINETY
        80: "\U00011c6a",  # 𑱪 BHAIKSUKI NUMBER EIGHTY
        70: "\U00011c69",  # 𑱩 BHAIKSUKI NUMBER SEVENTY
        60: "\U00011c68",  # 𑱨 BHAIKSUKI NUMBER SIXTY
        50: "\U00011c67",  # 𑱧 BHAIKSUKI NUMBER FIFTY
        40: "\U00011c66",  # 𑱦 BHAIKSUKI NUMBER FORTY
        30: "\U00011c65",  # 𑱥 BHAIKSUKI NUMBER THIRTY
        20: "\U00011c64",  # 𑱤 BHAIKSUKI NUMBER TWENTY
        10: "\U00011c63",  # 𑱣 BHAIKSUKI NUMBER TEN
        # Units: single-character number signs
        9: "\U00011c62",  # 𑱢 BHAIKSUKI NUMBER NINE
        8: "\U00011c61",  # 𑱡 BHAIKSUKI NUMBER EIGHT
        7: "\U00011c60",  # 𑱠 BHAIKSUKI NUMBER SEVEN
        6: "\U00011c5f",  # 𑱟 BHAIKSUKI NUMBER SIX
        5: "\U00011c5e",  # 𑱞 BHAIKSUKI NUMBER FIVE
        4: "\U00011c5d",  # 𑱝 BHAIKSUKI NUMBER FOUR
        3: "\U00011c5c",  # 𑱜 BHAIKSUKI NUMBER THREE
        2: "\U00011c5b",  # 𑱛 BHAIKSUKI NUMBER TWO
        1: "\U00011c5a",  # 𑱚 BHAIKSUKI NUMBER ONE
    }

    # Two-character hundred tokens come before single-character unit tokens so
    # that longest_match_from_numeral resolves them correctly.
    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Bhaiksuki numeral representation.

        Uses greedy additive decomposition, largest denomination first.
        Hundreds are encoded as a two-character sequence (unit sign + hundreds
        mark); decades and ones use single-character signs.

        Args:
            number: The Arabic number to convert.

        Returns:
            The Bhaiksuki string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Bhaiksuki._to_numeral(1)
            '𑱚'
            >>> Bhaiksuki._to_numeral(9)
            '𑱢'
            >>> Bhaiksuki._to_numeral(10)
            '𑱣'
            >>> Bhaiksuki._to_numeral(99)
            '𑱫𑱢'
            >>> Bhaiksuki._to_numeral(100)
            '𑱚𑱬'
            >>> Bhaiksuki._to_numeral(200)
            '𑱛𑱬'
            >>> Bhaiksuki._to_numeral(999)
            '𑱢𑱬𑱫𑱢'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Bhaiksuki numeral string to its Arabic integer value.

        Uses longest-match scanning so that two-character hundred tokens
        (unit sign + hundreds mark) are resolved before their constituent
        single-character unit signs.

        Args:
            numeral: The Bhaiksuki numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character or
                token.

        Examples:
            >>> Bhaiksuki._from_numeral('𑱚')
            1
            >>> Bhaiksuki._from_numeral('𑱢')
            9
            >>> Bhaiksuki._from_numeral('𑱣')
            10
            >>> Bhaiksuki._from_numeral('𑱫𑱢')
            99
            >>> Bhaiksuki._from_numeral('𑱚𑱬')
            100
            >>> Bhaiksuki._from_numeral('𑱛𑱬')
            200
            >>> Bhaiksuki._from_numeral('𑱢𑱬𑱫𑱢')
            999
            >>> Bhaiksuki._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Bhaiksuki character at position 0: '?'
        """
        return longest_match_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
