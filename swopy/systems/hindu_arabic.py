"""Hindu-Arabic numeral system converters.

This module implements numeral systems from the Hindu-Arabic script family.
Currently supports:

    Bakhshali  U+111E1-U+111F4  (twenty glyphs: units 1-9, decades 10-90,
                                  hundred, thousand)
    Arabic     (Python-native; pass-through converter)

Bakhshali (also called Sinhala Archaic) is a multiplicative-additive system
identical in structure to Brahmi: unit symbols (1-9) preceding a hundreds or
thousands symbol act as a multiplier (omitted when 1); each decade (10-90)
has its own symbol; ones are written directly.

Arabic numerals are the native representation in Python; conversion is a
pass-through with range and type checking only.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
)


class Arabic(System[float | Fraction | int, float | Fraction | int]):
    """Implements pass-through conversion between Python numeric types and Arabic
    numerals.

    - No Unicode block; Arabic numerals are the native representation in Python
    - The system accepts and returns int, float, or Fraction values unchanged;
      conversion is pure type and range checking

    Attributes:
        minimum: Minimum valid value (-infinity)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False - no natural bound exists
        encodings: UTF-8 and ASCII
    """

    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

    @classmethod
    def _to_numeral(cls, denotation: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting a denotation to a Arabic numeral.

        Examples:
            >>> Arabic.to_numeral(1)
            1
            >>> Arabic.to_numeral(42)
            42
        """
        return denotation

    @classmethod
    def _from_numeral(cls, numeral: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting an Arabic numeral to an denotation.

        Examples:
            >>> Arabic.from_numeral(1)
            1
            >>> Arabic.from_numeral(42)
            42
        """
        return numeral


class Bakhshali(System[str, int]):
    """Implements bidirectional conversion between integers and Bakhshali numerals.

    - Uses Unicode block U+111E1-U+111F4 within block U+111E0-U+111FF (twenty glyphs:
      units 1-9, decades 10-90, hundred 𑇳, thousand 𑇴)
    - The system is multiplicative-additive: unit symbols (1-9) preceding a hundreds or
      thousands symbol act as a multiplier (omitted when 1); each decade (10-90) has its
      own distinct symbol; the most significant group appears first (leftmost)

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (9,999)
        maximum_is_many: False - integers greater than 9,999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999
    maximum_is_many: ClassVar[bool] = False
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
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Bakhshali numerals.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10-90). Ones use a dedicated unit symbol (1-9).

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
        return multiplicative_additive_to_numeral(denotation, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Bakhshali numeral to an integer.

        Scans left-to-right. Unit symbols (𑇡-𑇩) accumulate in a buffer.
        When a hundreds (𑇳) or thousands (𑇴) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑇪-𑇲) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

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
