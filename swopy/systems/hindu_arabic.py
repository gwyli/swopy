"""Hindu-Arabic numeral system converters.

This module implements numeral systems from the Hindu-Arabic script family.
Currently supports:

    Bakhshali  U+111E1-U+111F4  (twenty glyphs: units 1–9, decades 10–90,
                                  hundred, thousand)
    Arabic     (Python-native; pass-through converter)

Bakhshali (also called Sinhala Archaic) is a multiplicative-additive system
identical in structure to Brahmi: unit symbols (1–9) preceding a hundreds or
thousands symbol act as a multiplier (omitted when 1); each decade (10–90)
has its own symbol; ones are written directly.

Arabic numerals are the native representation in Python; conversion is a
pass-through with range and type checking only.
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


class Arabic(System[float | Fraction | int, float | Fraction | int]):
    """Arabic numeral system converter.

    Implements conversion for Arabic numerals (0-9), the standard modern numeral
    system used worldwide. Since Arabic numerals are the native numeral representation
    in Python, this implementation serves as a pass-through converter.

    Attributes:
        to_numeral_map: Not used; integers are returned as-is.
        from_numeral_map: Not used; numbers are validated and returned as-is.
        minimum: Minimum representable value (-sys.float_info.max).
        maximum: Maximum representable value (sys.float_info.max).
        maximum_is_many: False, as the maximum is a precise limit.
    """

    @classmethod
    def _to_numeral(cls, number: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting a number to a Arabic numeral.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Arabic.to_numeral(1)
            1
            >>> Arabic.to_numeral(42)
            42
        """
        return number

    @classmethod
    def _from_numeral(cls, numeral: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting an Arabic numeral to an number.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

         Examples:
             >>> Arabic.from_numeral(1)
             1
             >>> Arabic.from_numeral(42)
             42
        """
        return numeral


class Bakhshali(System[str, int]):
    """Bakhshali (Sinhala Archaic) numeral system converter.

    Implements bidirectional conversion between integers and Bakhshali numeral
    strings. The system is multiplicative-additive, identical in structure to
    Brahmi: unit symbols (1–9) preceding a hundreds or thousands symbol act as
    a multiplier (omitted when 1); each decade (10–90) has its own symbol;
    ones are written directly. The most significant group appears first.

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

    The structure of a numeral is (each group optional):

        [unit_multiplier] 𑇴  — thousands (multiplier omitted when 1)
        [unit_multiplier] 𑇳  — hundreds  (multiplier omitted when 1)
        decade_symbol?        — one of 𑇪–𑇲 (10, 20, …, 90)
        unit_symbol?          — one of 𑇡–𑇩 (1–9)

    Examples:
        200  ->  𑇢𑇳  (two × 100)
        999  ->  𑇩𑇳𑇲𑇩  (nine × 100, ninety, nine)
        1996 ->  𑇴𑇩𑇳𑇲𑇦

    Attributes:
        _to_numeral_map: Mapping of the twenty base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Bakhshali glyphs have no ASCII equivalents.
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
        """Convert an Arabic integer to its Bakhshali numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10–90). Ones use a dedicated unit symbol (1–9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The Bakhshali string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Bakhshali._to_numeral(1)
            '𑇡'
            >>> Bakhshali._to_numeral(9)
            '𑇩'
            >>> Bakhshali._to_numeral(10)
            '𑇪'
            >>> Bakhshali._to_numeral(11)
            '𑇪𑇡'
            >>> Bakhshali._to_numeral(99)
            '𑇲𑇩'
            >>> Bakhshali._to_numeral(100)
            '𑇳'
            >>> Bakhshali._to_numeral(200)
            '𑇢𑇳'
            >>> Bakhshali._to_numeral(999)
            '𑇩𑇳𑇲𑇩'
            >>> Bakhshali._to_numeral(1000)
            '𑇴'
            >>> Bakhshali._to_numeral(1996)
            '𑇴𑇩𑇳𑇲𑇦'
            >>> Bakhshali._to_numeral(9999)
            '𑇩𑇴𑇩𑇳𑇲𑇩'
        """
        return multiplicative_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Bakhshali numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𑇡–𑇩) accumulate in a buffer.
        When a hundreds (𑇳) or thousands (𑇴) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑇪–𑇲) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Bakhshali numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Bakhshali._from_numeral('𑇩')
            9
            >>> Bakhshali._from_numeral('𑇩𑇳𑇲𑇩')
            999
            >>> Bakhshali._from_numeral('𑇴𑇩𑇳𑇲𑇦')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
