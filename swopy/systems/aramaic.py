"""Aramaic and related numeral system converters.

This module implements numeral systems from Aramaic and related cultures.
All systems are purely additive, using greedy decomposition for encoding
and character-sum for decoding.

Unicode blocks used:

    Imperial Aramaic                   U+10840-U+1085F
    Palmyrene                          U+10860-U+1087F
    Nabataean                          U+10880-U+108AF
    Hatran                             U+108E0-U+108FF
    Manichaean                         U+10AC0-U+10AFF
    Old Sogdian                        U+10F00-U+10F2F
    Sogdian                            U+10F30-U+10F6F
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import (
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


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


class ImperialAramaic(System[str, int]):
    """Imperial Aramaic numeral system converter.

    Implements bidirectional conversion between integers and Imperial Aramaic
    numeral strings using Unicode block U+10840–U+1085F. The system is purely
    additive and written right-to-left (largest denomination on the right),
    with dedicated signs for 1, 2, 3, 10, 20, 100, 1000, and 10000.
    The valid range is 1–99,999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999

    _to_numeral_map: Mapping[int, str] = {
        10000: "\U0001085f",  # 𐡟 IMPERIAL ARAMAIC NUMBER TEN THOUSAND
        1000: "\U0001085e",  # 𐡞 IMPERIAL ARAMAIC NUMBER ONE THOUSAND
        100: "\U0001085d",  # 𐡝 IMPERIAL ARAMAIC NUMBER ONE HUNDRED
        20: "\U0001085c",  # 𐡜 IMPERIAL ARAMAIC NUMBER TWENTY
        10: "\U0001085b",  # 𐡛 IMPERIAL ARAMAIC NUMBER TEN
        3: "\U0001085a",  # 𐡚 IMPERIAL ARAMAIC NUMBER THREE
        2: "\U00010859",  # 𐡙 IMPERIAL ARAMAIC NUMBER TWO
        1: "\U00010858",  # 𐡘 IMPERIAL ARAMAIC NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Imperial Aramaic numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> ImperialAramaic._to_numeral(1)
            '𐡘'
            >>> ImperialAramaic._to_numeral(3)
            '𐡚'
            >>> ImperialAramaic._to_numeral(10)
            '𐡛'
            >>> ImperialAramaic._to_numeral(100)
            '𐡝'
            >>> ImperialAramaic._to_numeral(1000)
            '𐡞'
            >>> ImperialAramaic._to_numeral(10000)
            '𐡟'
            >>> ImperialAramaic._to_numeral(999)
            '𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝'
            >>> ImperialAramaic._to_numeral(99999)
            '𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡞𐡟𐡟𐡟𐡟𐡟𐡟𐡟𐡟𐡟'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Imperial Aramaic numeral string to its Arabic integer value.

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
            >>> ImperialAramaic._from_numeral('𐡘')
            1
            >>> ImperialAramaic._from_numeral('𐡚')
            3
            >>> ImperialAramaic._from_numeral('𐡛')
            10
            >>> ImperialAramaic._from_numeral('𐡝')
            100
            >>> ImperialAramaic._from_numeral('𐡞')
            1000
            >>> ImperialAramaic._from_numeral('𐡟')
            10000
            >>> ImperialAramaic._from_numeral('𐡚𐡚𐡚𐡛𐡜𐡜𐡜𐡜𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝𐡝')
            999
            >>> ImperialAramaic._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid ImperialAramaic character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class Manichaean(System[str, int]):
    """Manichaean numeral system converter.

    Implements bidirectional conversion between integers and Manichaean numeral
    strings using Unicode block U+10AC0–U+10AFF. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 5, 10, 20, and 100. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010aef",  # 𐫯 MANICHAEAN NUMBER ONE HUNDRED
        20: "\U00010aee",  # 𐫮 MANICHAEAN NUMBER TWENTY
        10: "\U00010aed",  # 𐫭 MANICHAEAN NUMBER TEN
        5: "\U00010aec",  # 𐫬 MANICHAEAN NUMBER FIVE
        1: "\U00010aeb",  # 𐫫 MANICHAEAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Manichaean numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Manichaean._to_numeral(1)
            '𐫫'
            >>> Manichaean._to_numeral(5)
            '𐫬'
            >>> Manichaean._to_numeral(10)
            '𐫭'
            >>> Manichaean._to_numeral(11)
            '𐫫𐫭'
            >>> Manichaean._to_numeral(25)
            '𐫬𐫮'
            >>> Manichaean._to_numeral(100)
            '𐫯'
            >>> Manichaean._to_numeral(999)
            '𐫫𐫫𐫫𐫫𐫬𐫭𐫮𐫮𐫮𐫮𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Manichaean numeral string to its Arabic integer value.

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
            >>> Manichaean._from_numeral('𐫫')
            1
            >>> Manichaean._from_numeral('𐫬')
            5
            >>> Manichaean._from_numeral('𐫭')
            10
            >>> Manichaean._from_numeral('𐫫𐫭')
            11
            >>> Manichaean._from_numeral('𐫬𐫮')
            25
            >>> Manichaean._from_numeral('𐫯')
            100
            >>> Manichaean._from_numeral('𐫫𐫫𐫫𐫫𐫬𐫭𐫮𐫮𐫮𐫮𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯𐫯')
            999
            >>> Manichaean._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Manichaean character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class OldSogdian(System[str, int]):
    """Old Sogdian numeral system converter.

    Implements bidirectional conversion between integers and Old Sogdian numeral
    strings using Unicode block U+10F00–U+10F2F. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 2, 3, 4, 5, 10, 20, 30, and 100. The valid range
    is 1–999. (U+10F26 NUMBER ONE HALF is excluded.)

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010f25",  # 𐼥 OLD SOGDIAN NUMBER ONE HUNDRED
        30: "\U00010f24",  # 𐼤 OLD SOGDIAN NUMBER THIRTY
        20: "\U00010f23",  # 𐼣 OLD SOGDIAN NUMBER TWENTY
        10: "\U00010f22",  # 𐼢 OLD SOGDIAN NUMBER TEN
        5: "\U00010f21",  # 𐼡 OLD SOGDIAN NUMBER FIVE
        4: "\U00010f20",  # 𐼠 OLD SOGDIAN NUMBER FOUR
        3: "\U00010f1f",  # 𐼟 OLD SOGDIAN NUMBER THREE
        2: "\U00010f1e",  # 𐼞 OLD SOGDIAN NUMBER TWO
        1: "\U00010f1d",  # 𐼝 OLD SOGDIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Old Sogdian numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> OldSogdian._to_numeral(1)
            '𐼝'
            >>> OldSogdian._to_numeral(5)
            '𐼡'
            >>> OldSogdian._to_numeral(10)
            '𐼢'
            >>> OldSogdian._to_numeral(30)
            '𐼤'
            >>> OldSogdian._to_numeral(100)
            '𐼥'
            >>> OldSogdian._to_numeral(999)
            '𐼠𐼡𐼤𐼤𐼤𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Old Sogdian numeral string to its Arabic integer value.

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
            >>> OldSogdian._from_numeral('𐼝')
            1
            >>> OldSogdian._from_numeral('𐼡')
            5
            >>> OldSogdian._from_numeral('𐼢')
            10
            >>> OldSogdian._from_numeral('𐼤')
            30
            >>> OldSogdian._from_numeral('𐼥')
            100
            >>> OldSogdian._from_numeral('𐼠𐼡𐼤𐼤𐼤𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥𐼥')
            999
            >>> OldSogdian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid OldSogdian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class Sogdian(System[str, int]):
    """Sogdian numeral system converter.

    Implements bidirectional conversion between integers and Sogdian numeral
    strings using Unicode block U+10F30–U+10F6F. The system is purely additive
    and written right-to-left (largest denomination on the right), with
    dedicated signs for 1, 10, 20, and 100. The valid range is 1–999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010f54",  # 𐽔 SOGDIAN NUMBER ONE HUNDRED
        20: "\U00010f53",  # 𐽓 SOGDIAN NUMBER TWENTY
        10: "\U00010f52",  # 𐽒 SOGDIAN NUMBER TEN
        1: "\U00010f51",  # 𐽑 SOGDIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Sogdian numeral representation.

        Uses greedy additive decomposition, largest denomination first.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Sogdian._to_numeral(1)
            '𐽑'
            >>> Sogdian._to_numeral(10)
            '𐽒'
            >>> Sogdian._to_numeral(20)
            '𐽓'
            >>> Sogdian._to_numeral(21)
            '𐽑𐽓'
            >>> Sogdian._to_numeral(100)
            '𐽔'
            >>> Sogdian._to_numeral(999)
            '𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽒𐽓𐽓𐽓𐽓𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Sogdian numeral string to its Arabic integer value.

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
            >>> Sogdian._from_numeral('𐽑')
            1
            >>> Sogdian._from_numeral('𐽒')
            10
            >>> Sogdian._from_numeral('𐽓')
            20
            >>> Sogdian._from_numeral('𐽑𐽓')
            21
            >>> Sogdian._from_numeral('𐽔')
            100
            >>> Sogdian._from_numeral('𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽑𐽒𐽓𐽓𐽓𐽓𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔𐽔')
            999
            >>> Sogdian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Sogdian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
