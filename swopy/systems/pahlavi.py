"""Pahlavi numeral system converters.

This module implements numeral systems from the Pahlavi script family.
Currently supports:

    Inscriptional Parthian  U+10B40-U+10B5F  (eight glyphs: 1, 2, 3, 4, 10,
                                               20, 100, 1000)
    Inscriptional Pahlavi   U+10B60-U+10B7F  (eight glyphs: 1, 2, 3, 4, 10,
                                               20, 100, 1000)
    Psalter Pahlavi         U+10B80-U+10BAF  (seven glyphs: 1, 2, 3, 4, 10,
                                               20, 100)

All three systems are purely additive and written right-to-left (largest
denomination on the right). Number signs occupy the high end of each block;
the remaining code points encode alphabetic letters. Encoding uses greedy
decomposition followed by reversal; decoding reverses the input before
summing.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class InscriptionalParthian(System[str, int]):
    """Inscriptional Parthian numeral system converter.

    Implements bidirectional conversion between integers and Inscriptional
    Parthian numeral strings using Unicode block U+10B40-U+10B5F. The system
    is purely additive and written right-to-left (largest denomination on the
    right), with dedicated signs for 1, 2, 3, 4, 10, 20, 100, and 1000.
    The valid range is 1-9999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00010b5f",  # 𐭟 INSCRIPTIONAL PARTHIAN NUMBER ONE THOUSAND
        100: "\U00010b5e",  # 𐭞 INSCRIPTIONAL PARTHIAN NUMBER ONE HUNDRED
        20: "\U00010b5d",  # 𐭝 INSCRIPTIONAL PARTHIAN NUMBER TWENTY
        10: "\U00010b5c",  # 𐭜 INSCRIPTIONAL PARTHIAN NUMBER TEN
        4: "\U00010b5b",  # 𐭛 INSCRIPTIONAL PARTHIAN NUMBER FOUR
        3: "\U00010b5a",  # 𐭚 INSCRIPTIONAL PARTHIAN NUMBER THREE
        2: "\U00010b59",  # 𐭙 INSCRIPTIONAL PARTHIAN NUMBER TWO
        1: "\U00010b58",  # 𐭘 INSCRIPTIONAL PARTHIAN NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Inscriptional Parthian numeral.

        Uses greedy additive decomposition, largest denomination first, then
        reverses the result so the highest denomination appears rightmost.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> InscriptionalParthian._to_numeral(1)
            '𐭘'
            >>> InscriptionalParthian._to_numeral(4)
            '𐭛'
            >>> InscriptionalParthian._to_numeral(9)
            '𐭘𐭛𐭛'
            >>> InscriptionalParthian._to_numeral(20)
            '𐭝'
            >>> InscriptionalParthian._to_numeral(100)
            '𐭞'
            >>> InscriptionalParthian._to_numeral(1000)
            '𐭟'
            >>> InscriptionalParthian._to_numeral(1001)
            '𐭘𐭟'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Inscriptional Parthian numeral string to its Arabic integer value.

        Reverses the input (right-to-left -> left-to-right) then sums the
        values of each glyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> InscriptionalParthian._from_numeral('𐭘')
            1
            >>> InscriptionalParthian._from_numeral('𐭛')
            4
            >>> InscriptionalParthian._from_numeral('𐭘𐭛𐭛')
            9
            >>> InscriptionalParthian._from_numeral('𐭝')
            20
            >>> InscriptionalParthian._from_numeral('𐭟')
            1000
            >>> InscriptionalParthian._from_numeral('𐭘𐭟')
            1001
            >>> InscriptionalParthian._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid InscriptionalParthian character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class InscriptionalPahlavi(System[str, int]):
    """Inscriptional Pahlavi numeral system converter.

    Implements bidirectional conversion between integers and Inscriptional
    Pahlavi numeral strings using Unicode block U+10B60-U+10B7F. The system
    is purely additive and written right-to-left (largest denomination on the
    right), with dedicated signs for 1, 2, 3, 4, 10, 20, 100, and 1000.
    The valid range is 1-9999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00010b7f",  # 𐭿 INSCRIPTIONAL PAHLAVI NUMBER ONE THOUSAND
        100: "\U00010b7e",  # 𐭾 INSCRIPTIONAL PAHLAVI NUMBER ONE HUNDRED
        20: "\U00010b7d",  # 𐭽 INSCRIPTIONAL PAHLAVI NUMBER TWENTY
        10: "\U00010b7c",  # 𐭼 INSCRIPTIONAL PAHLAVI NUMBER TEN
        4: "\U00010b7b",  # 𐭻 INSCRIPTIONAL PAHLAVI NUMBER FOUR
        3: "\U00010b7a",  # 𐭺 INSCRIPTIONAL PAHLAVI NUMBER THREE
        2: "\U00010b79",  # 𐭹 INSCRIPTIONAL PAHLAVI NUMBER TWO
        1: "\U00010b78",  # 𐭸 INSCRIPTIONAL PAHLAVI NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Inscriptional Pahlavi numeral.

        Uses greedy additive decomposition, largest denomination first, then
        reverses the result so the highest denomination appears rightmost.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> InscriptionalPahlavi._to_numeral(1)
            '𐭸'
            >>> InscriptionalPahlavi._to_numeral(4)
            '𐭻'
            >>> InscriptionalPahlavi._to_numeral(9)
            '𐭸𐭻𐭻'
            >>> InscriptionalPahlavi._to_numeral(20)
            '𐭽'
            >>> InscriptionalPahlavi._to_numeral(100)
            '𐭾'
            >>> InscriptionalPahlavi._to_numeral(1000)
            '𐭿'
            >>> InscriptionalPahlavi._to_numeral(1001)
            '𐭸𐭿'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Inscriptional Pahlavi numeral string to its Arabic integer value.

        Reverses the input (right-to-left -> left-to-right) then sums the
        values of each glyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> InscriptionalPahlavi._from_numeral('𐭸')
            1
            >>> InscriptionalPahlavi._from_numeral('𐭻')
            4
            >>> InscriptionalPahlavi._from_numeral('𐭸𐭻𐭻')
            9
            >>> InscriptionalPahlavi._from_numeral('𐭽')
            20
            >>> InscriptionalPahlavi._from_numeral('𐭿')
            1000
            >>> InscriptionalPahlavi._from_numeral('𐭸𐭿')
            1001
            >>> InscriptionalPahlavi._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid InscriptionalPahlavi character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class PsalterPahlavi(System[str, int]):
    """Psalter Pahlavi numeral system converter.

    Implements bidirectional conversion between integers and Psalter Pahlavi
    numeral strings using Unicode block U+10B80-U+10BAF. The system is purely
    additive and written right-to-left (largest denomination on the right),
    with dedicated signs for 1, 2, 3, 4, 10, 20, and 100. The valid range is
    1-999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (999).
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 999

    _to_numeral_map: Mapping[int, str] = {
        100: "\U00010baf",  # 𐮯 PSALTER PAHLAVI NUMBER ONE HUNDRED
        20: "\U00010bae",  # 𐮮 PSALTER PAHLAVI NUMBER TWENTY
        10: "\U00010bad",  # 𐮭 PSALTER PAHLAVI NUMBER TEN
        4: "\U00010bac",  # 𐮬 PSALTER PAHLAVI NUMBER FOUR
        3: "\U00010bab",  # 𐮫 PSALTER PAHLAVI NUMBER THREE
        2: "\U00010baa",  # 𐮪 PSALTER PAHLAVI NUMBER TWO
        1: "\U00010ba9",  # 𐮩 PSALTER PAHLAVI NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Psalter Pahlavi numeral representation.

        Uses greedy additive decomposition, largest denomination first, then
        reverses the result so the highest denomination appears rightmost.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> PsalterPahlavi._to_numeral(1)
            '𐮩'
            >>> PsalterPahlavi._to_numeral(4)
            '𐮬'
            >>> PsalterPahlavi._to_numeral(9)
            '𐮩𐮬𐮬'
            >>> PsalterPahlavi._to_numeral(10)
            '𐮭'
            >>> PsalterPahlavi._to_numeral(100)
            '𐮯'
            >>> PsalterPahlavi._to_numeral(999)
            '𐮩𐮬𐮬𐮭𐮮𐮮𐮮𐮮𐮯𐮯𐮯𐮯𐮯𐮯𐮯𐮯𐮯'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Psalter Pahlavi numeral string to its Arabic integer value.

        Reverses the input (right-to-left -> left-to-right) then sums the
        values of each glyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> PsalterPahlavi._from_numeral('𐮩')
            1
            >>> PsalterPahlavi._from_numeral('𐮬')
            4
            >>> PsalterPahlavi._from_numeral('𐮩𐮬𐮬')
            9
            >>> PsalterPahlavi._from_numeral('𐮭')
            10
            >>> PsalterPahlavi._from_numeral('𐮯')
            100
            >>> PsalterPahlavi._from_numeral('𐮩𐮬𐮬𐮭𐮮𐮮𐮮𐮮𐮯𐮯𐮯𐮯𐮯𐮯𐮯𐮯𐮯')
            999
            >>> PsalterPahlavi._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid PsalterPahlavi character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
