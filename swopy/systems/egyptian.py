"""Egyptian and Coptic numeral system converters.

This module implements numeral systems from the Egyptian script family.
Currently supports:

    Egyptian Hieroglyphic  U+13000-U+1342F  (seven glyphs for powers of 10:
                                              1 to 1,000,000)
    Coptic Epact           U+102E0-U+102FF  (single-glyph units, decades, and
                                              centuries; 2-char thousands)

Egyptian Hieroglyphic is a purely additive system using greedy decomposition
for encoding and character-sum for decoding.  Values above 999,999 are treated
as "many" and capped at 1,000,000.

Coptic Epact is a ciphered additive system with unique glyphs for each unit,
decade, and century.  Thousands are encoded as a 2-character sequence (the
COPTIC EPACT THOUSANDS MARK followed by the unit glyph); longest-match
scanning is used for decoding, enforcing descending order.
"""

# ruff: noqa: RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    longest_match_from_numeral,
)


class Egyptian(System[str, int]):
    """Implements bidirectional conversion between integers and Egyptian Hieroglyphic
    numerals.

    - Uses Unicode block U+13000-U+1342F (seven glyphs for powers of 10:
      1 to 1,000,000)
    - The system is purely additive, written largest-to-smallest
    - Values above 999,999 are treated as "many" and capped at 1,000,000

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (1,000,000)
        maximum_is_many: True - 1,000,000 represents "many" in Egyptian notation
        encodings: UTF-8 only
    """

    _to_numeral_map: Mapping[int, str] = {
        1_000_000: "\U00013069",
        100_000: "\U00013153",
        10_000: "\U000130ad",
        1_000: "\U000131bc",
        100: "\U00013362",
        10: "\U00013386",
        1: "\U000133fa",
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 1_000_000

    maximum_is_many: ClassVar[bool] = True
    encodings: ClassVar[Encodings] = {"utf8"}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Converts an integer to an Egyptian numeral.

        Takes an integer and converts it to its Egyptian hieroglyph representation
        using the base-10 system of hieroglyphic symbols.

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Egyptian.to_numeral(1)
            '\U000133fa'
            >>> Egyptian.to_numeral(101)
            '\U00013362\U000133fa'
            >>> Egyptian.to_numeral(1000001)
            '\U00013069'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Converts an Egyptian numeral to an integer.

        Takes an Egyptian numeral and converts it to its integer equivalent
        by summing the values of each hieroglyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Egyptian.from_numeral("\U000133fa")  # Single unit hieroglyph
            1
            >>> Egyptian.from_numeral("\U00013386")  # Ten hieroglyph
            10
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class CopticEpact(System[str, int]):
    """Implements bidirectional conversion between integers and Coptic Epact numerals.

    - Uses Unicode block U+102E0-U+102FF
    - The system is ciphered additive with unique glyphs for each unit (1-9), decade
      (10-90), and century (100-900)
    - Thousands (1,000-9,000) are expressed as the COPTIC EPACT THOUSANDS MARK (U+102E0)
      prefixed before the corresponding unit glyph

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
        9000: "\U000102e0\U000102e9",  # 𐋠𐋩  thousands mark + NINE
        8000: "\U000102e0\U000102e8",  # 𐋠𐋨  thousands mark + EIGHT
        7000: "\U000102e0\U000102e7",  # 𐋠𐋧  thousands mark + SEVEN
        6000: "\U000102e0\U000102e6",  # 𐋠𐋦  thousands mark + SIX
        5000: "\U000102e0\U000102e5",  # 𐋠𐋥  thousands mark + FIVE
        4000: "\U000102e0\U000102e4",  # 𐋠𐋤  thousands mark + FOUR
        3000: "\U000102e0\U000102e3",  # 𐋠𐋣  thousands mark + THREE
        2000: "\U000102e0\U000102e2",  # 𐋠𐋢  thousands mark + TWO
        1000: "\U000102e0\U000102e1",  # 𐋠𐋡  thousands mark + ONE
        900: "\U000102fb",  # 𐋻  COPTIC EPACT NUMBER NINE HUNDRED
        800: "\U000102fa",  # 𐋺  COPTIC EPACT NUMBER EIGHT HUNDRED
        700: "\U000102f9",  # 𐋹  COPTIC EPACT NUMBER SEVEN HUNDRED
        600: "\U000102f8",  # 𐋸  COPTIC EPACT NUMBER SIX HUNDRED
        500: "\U000102f7",  # 𐋷  COPTIC EPACT NUMBER FIVE HUNDRED
        400: "\U000102f6",  # 𐋶  COPTIC EPACT NUMBER FOUR HUNDRED
        300: "\U000102f5",  # 𐋵  COPTIC EPACT NUMBER THREE HUNDRED
        200: "\U000102f4",  # 𐋴  COPTIC EPACT NUMBER TWO HUNDRED
        100: "\U000102f3",  # 𐋳  COPTIC EPACT NUMBER ONE HUNDRED
        90: "\U000102f2",  # 𐋲  COPTIC EPACT NUMBER NINETY
        80: "\U000102f1",  # 𐋱  COPTIC EPACT NUMBER EIGHTY
        70: "\U000102f0",  # 𐋰  COPTIC EPACT NUMBER SEVENTY
        60: "\U000102ef",  # 𐋯  COPTIC EPACT NUMBER SIXTY
        50: "\U000102ee",  # 𐋮  COPTIC EPACT NUMBER FIFTY
        40: "\U000102ed",  # 𐋭  COPTIC EPACT NUMBER FORTY
        30: "\U000102ec",  # 𐋬  COPTIC EPACT NUMBER THIRTY
        20: "\U000102eb",  # 𐋫  COPTIC EPACT NUMBER TWENTY
        10: "\U000102ea",  # 𐋪  COPTIC EPACT NUMBER TEN
        9: "\U000102e9",  # 𐋩  COPTIC EPACT DIGIT NINE
        8: "\U000102e8",  # 𐋨  COPTIC EPACT DIGIT EIGHT
        7: "\U000102e7",  # 𐋧  COPTIC EPACT DIGIT SEVEN
        6: "\U000102e6",  # 𐋦  COPTIC EPACT DIGIT SIX
        5: "\U000102e5",  # 𐋥  COPTIC EPACT DIGIT FIVE
        4: "\U000102e4",  # 𐋤  COPTIC EPACT DIGIT FOUR
        3: "\U000102e3",  # 𐋣  COPTIC EPACT DIGIT THREE
        2: "\U000102e2",  # 𐋢  COPTIC EPACT DIGIT TWO
        1: "\U000102e1",  # 𐋡  COPTIC EPACT DIGIT ONE
    }

    # Thousands tokens (2-char) must precede unit glyphs to ensure longest-match
    _from_numeral_map: Mapping[str, int] = {
        "\U000102e0\U000102e9": 9000,  # 𐋠𐋩
        "\U000102e0\U000102e8": 8000,  # 𐋠𐋨
        "\U000102e0\U000102e7": 7000,  # 𐋠𐋧
        "\U000102e0\U000102e6": 6000,  # 𐋠𐋦
        "\U000102e0\U000102e5": 5000,  # 𐋠𐋥
        "\U000102e0\U000102e4": 4000,  # 𐋠𐋤
        "\U000102e0\U000102e3": 3000,  # 𐋠𐋣
        "\U000102e0\U000102e2": 2000,  # 𐋠𐋢
        "\U000102e0\U000102e1": 1000,  # 𐋠𐋡
        "\U000102fb": 900,  # 𐋻
        "\U000102fa": 800,  # 𐋺
        "\U000102f9": 700,  # 𐋹
        "\U000102f8": 600,  # 𐋸
        "\U000102f7": 500,  # 𐋷
        "\U000102f6": 400,  # 𐋶
        "\U000102f5": 300,  # 𐋵
        "\U000102f4": 200,  # 𐋴
        "\U000102f3": 100,  # 𐋳
        "\U000102f2": 90,  # 𐋲
        "\U000102f1": 80,  # 𐋱
        "\U000102f0": 70,  # 𐋰
        "\U000102ef": 60,  # 𐋯
        "\U000102ee": 50,  # 𐋮
        "\U000102ed": 40,  # 𐋭
        "\U000102ec": 30,  # 𐋬
        "\U000102eb": 20,  # 𐋫
        "\U000102ea": 10,  # 𐋪
        "\U000102e9": 9,  # 𐋩
        "\U000102e8": 8,  # 𐋨
        "\U000102e7": 7,  # 𐋧
        "\U000102e6": 6,  # 𐋦
        "\U000102e5": 5,  # 𐋥
        "\U000102e4": 4,  # 𐋤
        "\U000102e3": 3,  # 𐋣
        "\U000102e2": 2,  # 𐋢
        "\U000102e1": 1,  # 𐋡
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Coptic Epact numeral representation.

        Uses greedy additive decomposition. Thousands are encoded as a 2-character
        sequence: the COPTIC EPACT THOUSANDS MARK (𐋠) followed by the unit glyph
        for the thousands digit.

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> CopticEpact._to_numeral(1)
            '𐋡'
            >>> CopticEpact._to_numeral(9)
            '𐋩'
            >>> CopticEpact._to_numeral(10)
            '𐋪'
            >>> CopticEpact._to_numeral(99)
            '𐋲𐋩'
            >>> CopticEpact._to_numeral(999)
            '𐋻𐋲𐋩'
            >>> CopticEpact._to_numeral(1000)
            '𐋠𐋡'
            >>> CopticEpact._to_numeral(1492)
            '𐋠𐋡𐋶𐋲𐋢'
            >>> CopticEpact._to_numeral(9999)
            '𐋠𐋩𐋻𐋲𐋩'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Coptic Epact numeral string to its Arabic integer value.

        Uses longest-match scanning so that the 2-character thousands sequences
        (𐋠 + digit) are consumed before the bare digit glyphs. Values must appear
        in non-increasing order (thousands before hundreds before tens before units).

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid or out of order.

        Examples:
            >>> CopticEpact._from_numeral('𐋡')
            1
            >>> CopticEpact._from_numeral('𐋲𐋩')
            99
            >>> CopticEpact._from_numeral('𐋻𐋲𐋩')
            999
            >>> CopticEpact._from_numeral('𐋠𐋡')
            1000
            >>> CopticEpact._from_numeral('𐋠𐋡𐋶𐋲𐋢')
            1492
            >>> CopticEpact._from_numeral('𐋠𐋩𐋻𐋲𐋩')
            9999
            >>> CopticEpact._from_numeral('𐋪𐋠𐋡')
            Traceback (most recent call last):
                ...
            ValueError: Invalid CopticEpact sequence: '𐋠𐋡' cannot follow a smaller value.
        """
        return longest_match_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls.__name__,
            enforce_descending=True,
            initial_max=int(cls.maximum) + 1,
        )
