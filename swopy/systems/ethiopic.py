"""Ethiopic numeral system converters.

This module implements numeral systems from the Ethiopic script family.
Currently supports:

    Ethiopic  U+1369-U+137C  (digit glyphs 1-9 at U+1369-U+1371; decade
                               signs 10-90 at U+1372-U+137A; hundreds sign
                               U+137B; ten-thousands sign U+137C)

Ethiopic numerals are a two-tier multiplicative-additive system.  Dedicated
digit glyphs cover 1-9; dedicated decade signs cover 10-90; a hundreds sign
(፻, U+137B) and a ten-thousands sign (፼, U+137C) act as multipliers.

Encoding rules:
  - Numbers 1-9: use the corresponding digit glyph directly.
  - Numbers 10-90: use the corresponding decade glyph directly.
  - Numbers 100-9,999: the hundreds coefficient (1-99) is encoded as a
    sub-100 number placed immediately before ፻; the coefficient 1 is omitted
    (100 = ፻, not ፩፻).
  - Numbers 10,000-99,999,999: the coefficient (1-9,999) is encoded as a
    sub-10,000 number placed before ፼; the remainder (0-9,999) follows ፼.

Decoding reverses the process by splitting at ፼ and ፻ anchors.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral

_HUNDRED = "\u137b"  # ፻  ETHIOPIC NUMBER HUNDRED
_MYRIAD = "\u137c"  # ፼  ETHIOPIC NUMBER TEN THOUSAND

# Additive map for sub-100 encoding/decoding (digits 1-9 and decades 10-90)
_SUB100_MAP: Mapping[int, str] = {
    90: "\u137a",  # ፺
    80: "\u1379",  # ፹
    70: "\u1378",  # ፸
    60: "\u1377",  # ፷
    50: "\u1376",  # ፶
    40: "\u1375",  # ፵
    30: "\u1374",  # ፴
    20: "\u1373",  # ፳
    10: "\u1372",  # ፲
    9: "\u1371",  # ፱
    8: "\u1370",  # ፰
    7: "\u136f",  # ፯
    6: "\u136e",  # ፮
    5: "\u136d",  # ፭
    4: "\u136c",  # ፬
    3: "\u136b",  # ፫
    2: "\u136a",  # ፪
    1: "\u1369",  # ፩
}

_SUB100_FROM: Mapping[str, int] = {v: k for k, v in _SUB100_MAP.items()}


def _encode_sub100(n: int) -> str:
    """Encode an integer 1-99 using Ethiopic digit and decade glyphs."""
    result = ""
    if n >= 10:  # noqa: PLR2004
        tens = (n // 10) * 10
        result += _SUB100_MAP[tens]
        n %= 10
    if n:
        result += _SUB100_MAP[n]
    return result


def _decode_sub100(numeral: str, system_name: str) -> int:
    """Decode a string of Ethiopic digit/decade glyphs (no ፻ or ፼)."""
    return char_sum_from_numeral(numeral, _SUB100_FROM, system_name)


def _encode_sub9999(n: int) -> str:
    """Encode an integer 1-9999 using Ethiopic sub-hundred encoding."""
    result = ""
    hundreds = n // 100
    remainder = n % 100
    if hundreds:
        if hundreds != 1:
            result += _encode_sub100(hundreds)
        result += _HUNDRED
    result += _encode_sub100(remainder) if remainder else ""
    return result


def _decode_sub9999(numeral: str, system_name: str) -> int:
    """Decode an Ethiopic sub-myriad numeral (may contain ፻ but not ፼)."""
    if not numeral:
        return 0
    if _HUNDRED in numeral:
        idx = numeral.index(_HUNDRED)
        coeff = _decode_sub100(numeral[:idx], system_name) if idx else 1
        remainder = _decode_sub100(numeral[idx + 1 :], system_name)
        return coeff * 100 + remainder
    return _decode_sub100(numeral, system_name)


class Ethiopic(System[str, int]):
    """Implements bidirectional conversion between integers and Ethiopic numerals.

    - Uses Unicode block U+1369-U+137C
    - The system is two-tier multiplicative-additive: digit glyphs (1-9) combine with
      decade glyphs (10-90), a hundreds sign (፻), and a ten-thousands sign (፼) acting
      as multipliers
    - Hundreds and ten-thousands coefficients of 1 are omitted

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (99,999,999)
        maximum_is_many: False - integers greater than 99,999,999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        **_SUB100_MAP,
        100: _HUNDRED,
        10000: _MYRIAD,
    }

    _from_numeral_map: Mapping[str, int] = {
        **_SUB100_FROM,
        _HUNDRED: 100,
        _MYRIAD: 10000,
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to Ethiopic numerals.

        Denotations >= 10,000 are expressed as ``encode_sub9999(coefficient) + ፼``
        followed by ``encode_sub9999(remainder)``.  Within each sub-10,000
        segment, hundreds use ``encode_sub100(coefficient) + ፻`` with the
        coefficient omitted when equal to 1.

        Examples:
            >>> Ethiopic._to_numeral(1)
            '፩'
            >>> Ethiopic._to_numeral(10)
            '፲'
            >>> Ethiopic._to_numeral(99)
            '፺፱'
            >>> Ethiopic._to_numeral(100)
            '፻'
            >>> Ethiopic._to_numeral(200)
            '፪፻'
            >>> Ethiopic._to_numeral(1000)
            '፲፻'
            >>> Ethiopic._to_numeral(9999)
            '፺፱፻፺፱'
            >>> Ethiopic._to_numeral(10000)
            '፼'
            >>> Ethiopic._to_numeral(20000)
            '፪፼'
            >>> Ethiopic._to_numeral(99999999)
            '፺፱፻፺፱፼፺፱፻፺፱'
        """
        myriads = denotation // 10000
        remainder = denotation % 10000
        result = ""
        if myriads:
            if myriads != 1:
                result += _encode_sub9999(myriads)
            result += _MYRIAD
        result += _encode_sub9999(remainder) if remainder else ""
        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ethiopic numeral to an integer.

        Splits at ፼ (if present): the portion before is decoded as a
        sub-9999 coefficient multiplied by 10,000; the portion after is
        decoded as the remainder.  Each sub-9999 segment is further split
        at ፻ to extract the hundreds coefficient.

        Examples:
            >>> Ethiopic._from_numeral('፩')
            1
            >>> Ethiopic._from_numeral('፲')
            10
            >>> Ethiopic._from_numeral('፺፱')
            99
            >>> Ethiopic._from_numeral('፻')
            100
            >>> Ethiopic._from_numeral('፪፻')
            200
            >>> Ethiopic._from_numeral('፲፻')
            1000
            >>> Ethiopic._from_numeral('፺፱፻፺፱')
            9999
            >>> Ethiopic._from_numeral('፼')
            10000
            >>> Ethiopic._from_numeral('፪፼')
            20000
            >>> Ethiopic._from_numeral('፺፱፻፺፱፼፺፱፻፺፱')
            99999999
            >>> Ethiopic._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Ethiopic character: '?'
        """
        if _MYRIAD in numeral:
            idx = numeral.index(_MYRIAD)
            myriad_coeff = _decode_sub9999(numeral[:idx], cls.__name__) if idx else 1
            remainder = _decode_sub9999(numeral[idx + 1 :], cls.__name__)
            return myriad_coeff * 10000 + remainder
        return _decode_sub9999(numeral, cls.__name__)
