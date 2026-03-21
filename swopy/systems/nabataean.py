# ruff: noqa: RUF002
"""Nabataean numeral system converters.

This module implements numeral systems from the Nabataean script family.
Currently supports:

    Nabataean  U+10880-U+108AF  (nine glyphs: 1, 2, 3, 4, 5, 10, 20, 100;
                                  alternate cruciform form of 4 at U+108AB)

Nabataean is a purely additive system using greedy decomposition for encoding
and character-sum for decoding.  An alternative cruciform form of 4 (U+108AB)
is accepted as input alongside the standard form (U+108AA).
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Nabataean(System[str, int]):
    """Nabataean numeral system converter.

    Implements bidirectional conversion between integers and Nabataean numeral
    strings using Unicode block U+10880–U+108AF. The system is purely additive
    with dedicated signs for 1, 2, 3, 4, 5, 10, 20, and 100. An alternative
    cruciform form of 4 (U+108AB) is accepted as input. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U000108af",  # 𐢯 NABATAEAN NUMBER ONE HUNDRED
        20: "\U000108ae",  # 𐢮 NABATAEAN NUMBER TWENTY
        10: "\U000108ad",  # 𐢭 NABATAEAN NUMBER TEN
        5: "\U000108ac",  # 𐢬 NABATAEAN NUMBER FIVE
        4: "\U000108aa",  # 𐢪 NABATAEAN NUMBER FOUR
        3: "\U000108a9",  # 𐢩 NABATAEAN NUMBER THREE
        2: "\U000108a8",  # 𐢨 NABATAEAN NUMBER TWO
        1: "\U000108a7",  # 𐢧 NABATAEAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {
        "\U000108af": 100,  # 𐢯 NABATAEAN NUMBER ONE HUNDRED
        "\U000108ae": 20,  # 𐢮 NABATAEAN NUMBER TWENTY
        "\U000108ad": 10,  # 𐢭 NABATAEAN NUMBER TEN
        "\U000108ac": 5,  # 𐢬 NABATAEAN NUMBER FIVE
        "\U000108ab": 4,  # 𐢫 NABATAEAN CRUCIFORM NUMBER FOUR (alternate form)
        "\U000108aa": 4,  # 𐢪 NABATAEAN NUMBER FOUR
        "\U000108a9": 3,  # 𐢩 NABATAEAN NUMBER THREE
        "\U000108a8": 2,  # 𐢨 NABATAEAN NUMBER TWO
        "\U000108a7": 1,  # 𐢧 NABATAEAN NUMBER ONE
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Nabataean numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Nabataean._to_numeral(1)
            '𐢧'
            >>> Nabataean._to_numeral(4)
            '𐢪'
            >>> Nabataean._to_numeral(15)
            '𐢭𐢬'
            >>> Nabataean._to_numeral(104)
            '𐢯𐢪'
            >>> Nabataean._to_numeral(999)
            '𐢯𐢯𐢯𐢯𐢯𐢯𐢯𐢯𐢯𐢮𐢮𐢮𐢮𐢭𐢬𐢪'
        """
        return greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Nabataean numeral string to its Arabic integer value.

        Accepts both the standard form (U+108AA) and the cruciform form
        (U+108AB) for the value 4. Sums the values of each glyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Nabataean._from_numeral('𐢧')
            1
            >>> Nabataean._from_numeral('𐢪')
            4
            >>> Nabataean._from_numeral('𐢫')
            4
            >>> Nabataean._from_numeral('𐢭𐢬')
            15
            >>> Nabataean._from_numeral('𐢯𐢪')
            104
            >>> Nabataean._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Nabataean character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
