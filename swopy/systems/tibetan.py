"""Tibetan and related numeral system converters.

This module implements numeral systems from the Tibetan cultural sphere.
Currently supports:

    Tangut  U+17000-U+187FF  (specific glyphs listed below)

Tangut is a multiplicative-additive system with myriad (10,000) grouping.
Digits 1-9 have unique glyphs; multipliers for 10, 100, 1,000 and 10,000
are separate characters. Zero is omitted from normal use (place values are
simply skipped when their digit is zero).

Encoding rules:

    Tens place  - digit always explicit, even for 1: e.g. 10 = [1][x10]
    Other places - digit 1 is omitted; digit 2-9 precedes the multiplier
    Myriad      - the full sub-myriad coefficient (1-9999) precedes [x10000]
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System


class Tangut(System[str, int]):
    """Tangut numeral system converter.

    Implements bidirectional conversion between integers and Tangut numeral
    strings. The system is multiplicative-additive with a myriad base:

    - Digits 1-9 are represented by unique glyphs.
    - Multipliers x10, x100, x1000, x10000 are separate characters.
    - The tens place always carries an explicit digit (including 1).
    - Hundreds, thousands and myriad coefficients omit the digit when it is 1.
    - Zero places are skipped entirely (no zero glyph in normal use).
    - The myriad (x10000) coefficient can itself be a sub-myriad number (1-9999).

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999,999).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999

    encodings: ClassVar[Encodings] = {"utf8"}

    # Individual digit glyphs (1-9)
    _to_numeral_map: Mapping[int, str] = {
        1: "\U00017f11",  # 𗼑  Tangut digit one
        2: "\U000180ae",  # 𘂮  Tangut digit two
        3: "\U00018555",  # 𘕕  Tangut digit three
        4: "\U00017943",  # 𗥃  Tangut digit four
        5: "\U000173c1",  # 𗏁  Tangut digit five
        6: "\U00017901",  # 𗤁  Tangut digit six
        7: "\U000175d9",  # 𗗙  Tangut digit seven
        8: "\U0001824b",  # 𘉋  Tangut digit eight
        9: "\U000178ad",  # 𗢭  Tangut digit nine
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    # Multiplier glyphs
    _multipliers: ClassVar[Mapping[int, str]] = {
        10000: "\U00017457",  # 𗑗  Tangut myriad (x10,000)
        1000: "\U000170d4",  # 𗃔  Tangut thousand (x1,000)
        100: "\U000172da",  # 𗋚  Tangut hundred (x100)
        10: "\U00017c17",  # 𗰗  Tangut ten (x10)
    }

    # Sub-myriad multipliers only (used in the parser)
    _sub_multipliers: ClassVar[Mapping[str, int]] = {
        "\U000170d4": 1000,
        "\U000172da": 100,
        "\U00017c17": 10,
    }

    @classmethod
    def _encode_sub_myriad(cls, number: int) -> str:
        """Encode an integer in 1-9999 as a Tangut sub-myriad string.

        Args:
            number: Integer in the range 1-9999.

        Returns:
            The Tangut numeral string for ``number``.
        """
        result = ""
        thousands, number = divmod(number, 1000)
        if thousands:
            if thousands > 1:
                result += cls._to_numeral_map[thousands]
            result += cls._multipliers[1000]
        hundreds, number = divmod(number, 100)
        if hundreds:
            if hundreds > 1:
                result += cls._to_numeral_map[hundreds]
            result += cls._multipliers[100]
        tens, number = divmod(number, 10)
        if tens:
            result += cls._to_numeral_map[tens]  # always explicit
            result += cls._multipliers[10]
        if number:
            result += cls._to_numeral_map[number]
        return result

    @classmethod
    def _parse_sub_myriad(cls, numeral: str) -> int:
        """Parse a Tangut sub-myriad numeral string (no myriad glyph present).

        Scans left-to-right. A digit character followed by a sub-myriad
        multiplier contributes ``digit * multiplier``; a lone multiplier
        contributes ``1 * multiplier``; a lone digit contributes its value.

        Args:
            numeral: Tangut numeral string containing only digit and
                sub-myriad multiplier glyphs.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If an unrecognised character is encountered.
        """
        total = 0
        i = 0
        while i < len(numeral):
            c = numeral[i]
            if c in cls._from_numeral_map:
                digit = cls._from_numeral_map[c]
                i += 1
                if i < len(numeral) and numeral[i] in cls._sub_multipliers:
                    total += digit * cls._sub_multipliers[numeral[i]]
                    i += 1
                else:
                    total += digit
            elif c in cls._sub_multipliers:
                total += cls._sub_multipliers[c]
                i += 1
            else:
                raise ValueError(f"Invalid {cls.__name__} character: {c!r}")
        return total

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Tangut numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + myriad``,
        where the coefficient (1-9999) is itself encoded by ``_encode_sub_myriad``.
        The remainder (0-9999) is appended directly.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Tangut._to_numeral(1)
            '𗼑'
            >>> Tangut._to_numeral(10)
            '𗼑𗰗'
            >>> Tangut._to_numeral(15)
            '𗼑𗰗𗏁'
            >>> Tangut._to_numeral(100)
            '𗋚'
            >>> Tangut._to_numeral(200)
            '𘂮𗋚'
            >>> Tangut._to_numeral(1005)
            '𗃔𗏁'
            >>> Tangut._to_numeral(10000)
            '𗼑𗑗'
            >>> Tangut._to_numeral(20000)
            '𘂮𗑗'
            >>> Tangut._to_numeral(100000)
            '𗼑𗰗𗑗'
            >>> Tangut._to_numeral(99999999)
            '𗢭𗃔𗢭𗋚𗢭𗰗𗢭𗑗𗢭𗃔𗢭𗋚𗢭𗰗𗢭'
        """
        myriads, remainder = divmod(number, 10000)
        result = ""
        if myriads:
            result += cls._encode_sub_myriad(myriads)
            result += cls._multipliers[10000]
        if remainder:
            result += cls._encode_sub_myriad(remainder)
        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Tangut numeral string to its Arabic integer value.

        Splits at the myriad glyph (if present): the portion before it is
        parsed as a sub-myriad coefficient and multiplied by 10,000; the
        portion after is parsed as the remainder. If no myriad glyph is
        present, the whole string is parsed as a sub-myriad number.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Tangut._from_numeral('𗼑')
            1
            >>> Tangut._from_numeral('𗼑𗰗')
            10
            >>> Tangut._from_numeral('𗼑𗰗𗏁')
            15
            >>> Tangut._from_numeral('𗋚')
            100
            >>> Tangut._from_numeral('𗃔𗏁')
            1005
            >>> Tangut._from_numeral('𗼑𗑗')
            10000
            >>> Tangut._from_numeral('𗼑𗰗𗑗')
            100000
            >>> Tangut._from_numeral('𗢭𗃔𗢭𗋚𗢭𗰗𗢭𗑗𗢭𗃔𗢭𗋚𗢭𗰗𗢭')
            99999999
            >>> Tangut._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Tangut character: '?'
        """
        myriad_glyph = cls._multipliers[10000]
        if myriad_glyph in numeral:
            idx = numeral.index(myriad_glyph)
            coeff = cls._parse_sub_myriad(numeral[:idx]) if idx > 0 else 1
            remainder = (
                cls._parse_sub_myriad(numeral[idx + 1 :])
                if idx + 1 < len(numeral)
                else 0
            )
            return coeff * 10000 + remainder
        return cls._parse_sub_myriad(numeral)
