"""Mesopotamian numeral system converters.

This module implements numeral systems from Mesopotamian and related cultures:
Cuneiform, Palmyrene, Hatran, and Nabataean. All four are purely additive
systems using greedy decomposition for encoding and character-sum for decoding.

Unicode blocks used:

    Palmyrene                          U+10860-U+1087F
    Hatran                             U+108E0-U+108FF
    Nabataean                          U+10880-U+108AF
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import char_sum_from_numeral, greedy_additive_to_numeral


class Palmyrene(System[str, int]):
    """Palmyrene numeral system converter.

    Implements bidirectional conversion between integers and Palmyrene numeral
    strings using Unicode block U+10860–U+1087F. The system is purely additive
    with dedicated signs for 1, 2, 3, 4, 5, 10, and 20. No sign for 100 exists
    in the Unicode block, so the valid range is 1–99.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99

    _to_numeral_map: Mapping[int, str] = {
        20: "\U0001087f",  # 𐡿 PALMYRENE NUMBER TWENTY
        10: "\U0001087e",  # 𐡾 PALMYRENE NUMBER TEN
        5: "\U0001087d",  # 𐡽 PALMYRENE NUMBER FIVE
        4: "\U0001087c",  # 𐡼 PALMYRENE NUMBER FOUR
        3: "\U0001087b",  # 𐡻 PALMYRENE NUMBER THREE
        2: "\U0001087a",  # 𐡺 PALMYRENE NUMBER TWO
        1: "\U00010879",  # 𐡹 PALMYRENE NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Palmyrene numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Palmyrene._to_numeral(1)
            '𐡹'
            >>> Palmyrene._to_numeral(15)
            '𐡾𐡽'
            >>> Palmyrene._to_numeral(20)
            '𐡿'
            >>> Palmyrene._to_numeral(21)
            '𐡿𐡹'
            >>> Palmyrene._to_numeral(99)
            '𐡿𐡿𐡿𐡿𐡾𐡽𐡼'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Palmyrene numeral string to its Arabic integer value.

        Sums the values of each glyph in the string.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Palmyrene._from_numeral('𐡹')
            1
            >>> Palmyrene._from_numeral('𐡾𐡽')
            15
            >>> Palmyrene._from_numeral('𐡿')
            20
            >>> Palmyrene._from_numeral('𐡿𐡹')
            21
            >>> Palmyrene._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Palmyrene character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Hatran(System[str, int]):
    """Hatran numeral system converter.

    Implements bidirectional conversion between integers and Hatran numeral
    strings using Unicode block U+108E0–U+108FF. The system is purely additive
    with dedicated signs for 1, 5, 10, 20, and 100. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U000108ff",  # 𐣿 HATRAN NUMBER ONE HUNDRED
        20: "\U000108fe",  # 𐣾 HATRAN NUMBER TWENTY
        10: "\U000108fd",  # 𐣽 HATRAN NUMBER TEN
        5: "\U000108fc",  # 𐣼 HATRAN NUMBER FIVE
        1: "\U000108fb",  # 𐣻 HATRAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Hatran numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Hatran._to_numeral(1)
            '𐣻'
            >>> Hatran._to_numeral(6)
            '𐣼𐣻'
            >>> Hatran._to_numeral(100)
            '𐣿'
            >>> Hatran._to_numeral(125)
            '𐣿𐣾𐣼'
            >>> Hatran._to_numeral(999)
            '𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣿𐣾𐣾𐣾𐣾𐣽𐣼𐣻𐣻𐣻𐣻'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Hatran numeral string to its Arabic integer value.

        Sums the values of each glyph in the string.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Hatran._from_numeral('𐣻')
            1
            >>> Hatran._from_numeral('𐣼𐣻')
            6
            >>> Hatran._from_numeral('𐣿')
            100
            >>> Hatran._from_numeral('𐣿𐣾𐣼')
            125
            >>> Hatran._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Hatran character: '?'
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


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
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Nabataean numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

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
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

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
