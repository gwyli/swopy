"""Phoenician numeral system converters.

This module implements numeral systems from the Phoenician script family.
Currently supports:

    Phoenician  U+10916-U+1091B

Phoenician is a purely additive system using greedy decomposition for encoding
and character-sum for decoding.  No sign exists for 5, 50, or 1000, so values
such as 4-9 are expressed by combining smaller signs (e.g. 9 = 3+3+3 = 𐤛𐤛𐤛).
The valid range is 1-999.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Phoenician(System[str, int]):
    """Implements bidirectional conversion between integers and Phoenician numerals.

    - Uses Unicode block U+10916-U+1091B
    - The system is purely additive with dedicated signs for 1, 2, 3, 10, 20, and 100
    - No sign exists for 5 or 50, so values like 9 are expressed by repeating
      smaller signs (e.g. 9 = 3+3+3)

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
        100: "\U00010919",  # 𐤙  PHOENICIAN NUMBER ONE HUNDRED
        20: "\U00010918",  # 𐤘  PHOENICIAN NUMBER TWENTY
        10: "\U00010917",  # 𐤗  PHOENICIAN NUMBER TEN
        3: "\U0001091b",  # 𐤛  PHOENICIAN NUMBER THREE
        2: "\U0001091a",  # 𐤚  PHOENICIAN NUMBER TWO
        1: "\U00010916",  # 𐤖  PHOENICIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to a Phoenician numeral.

        Uses greedy additive decomposition, largest denomination first. Values
        without a dedicated sign (e.g. 4-9) are expressed by combining the
        largest available signs (e.g. 9 = 3+3+3 = 𐤛𐤛𐤛).

        Examples:
            >>> Phoenician._to_numeral(1)
            '𐤖'
            >>> Phoenician._to_numeral(4)
            '𐤛𐤖'
            >>> Phoenician._to_numeral(9)
            '𐤛𐤛𐤛'
            >>> Phoenician._to_numeral(10)
            '𐤗'
            >>> Phoenician._to_numeral(19)
            '𐤗𐤛𐤛𐤛'
            >>> Phoenician._to_numeral(100)
            '𐤙'
            >>> Phoenician._to_numeral(999)
            '𐤙𐤙𐤙𐤙𐤙𐤙𐤙𐤙𐤙𐤘𐤘𐤘𐤘𐤗𐤛𐤛𐤛'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Phoenician numeral to an integer

        Sums the values of each glyph in the string.

        Examples:
            >>> Phoenician._from_numeral('𐤖')
            1
            >>> Phoenician._from_numeral('𐤛𐤖')
            4
            >>> Phoenician._from_numeral('𐤛𐤛𐤛')
            9
            >>> Phoenician._from_numeral('𐤗𐤛𐤛𐤛')
            19
            >>> Phoenician._from_numeral('𐤙')
            100
            >>> Phoenician._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Phoenician character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
