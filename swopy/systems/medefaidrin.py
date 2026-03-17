"""Medefaidrin numeral system converters.

This module implements numeral systems from the Medefaidrin script family,
used in Nigeria.
Currently supports:

    Medefaidrin  U+16E40-U+16E9F  (twenty digit glyphs: 0-19,
                                    U+16E80-U+16E93; alternate forms
                                    for 1-3 at U+16E94-U+16E96)

Medefaidrin is a positional base-20 (vigesimal) system, analogous to the
Arabic base-10 system. Each digit position represents a power of 20; the
twenty unique glyphs encode values 0-19. Numbers are written most-significant
digit first (left-to-right). Alternate digit forms for 1, 2, and 3
(U+16E94-U+16E96) are accepted as input but not emitted on output.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System


class Medefaidrin(System[str, int]):
    """Medefaidrin vigesimal (base-20) numeral system converter.

    Implements bidirectional conversion between non-negative integers and
    Medefaidrin numeral strings using Unicode block U+16E40-U+16E9F. The
    system is positional in base 20, with twenty unique digit glyphs encoding
    values 0-19 at U+16E80-U+16E93. Numbers are written most-significant
    digit first (left-to-right). Zero is represented by the single glyph
    at U+16E80.

    Alternate glyph forms for 1, 2, and 3 (U+16E94-U+16E96) are accepted
    as input but are never emitted on output.

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (+infinity).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x16E80 + i) for i in range(20)}

    _from_numeral_map: Mapping[str, int] = {
        **{chr(0x16E80 + i): i for i in range(20)},
        "\U00016e94": 1,  # 𛺔 MEDEFAIDRIN DIGIT ONE ALTERNATE FORM
        "\U00016e95": 2,  # 𛺕 MEDEFAIDRIN DIGIT TWO ALTERNATE FORM
        "\U00016e96": 3,  # 𛺖 MEDEFAIDRIN DIGIT THREE ALTERNATE FORM
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert a non-negative integer to its Medefaidrin base-20 representation.

        Encodes ``number`` in base 20, emitting the most-significant vigesimal
        digit first. Zero is represented by the single glyph 𛺀.

        Args:
            number: The non-negative integer to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Medefaidrin._to_numeral(0)
            '\U00016e80'
            >>> Medefaidrin._to_numeral(1)
            '\U00016e81'
            >>> Medefaidrin._to_numeral(19)
            '\U00016e93'
            >>> Medefaidrin._to_numeral(20)
            '\U00016e81\U00016e80'
            >>> Medefaidrin._to_numeral(42)
            '\U00016e82\U00016e82'
            >>> Medefaidrin._to_numeral(400)
            '\U00016e81\U00016e80\U00016e80'
        """
        if number == 0:
            return cls._to_numeral_map[0]
        parts: list[str] = []
        while number:
            number, remainder = divmod(number, 20)
            parts.append(cls._to_numeral_map[remainder])
        return "".join(reversed(parts))

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Medefaidrin numeral string to its integer value.

        Scans each glyph left-to-right, accumulating
        ``total = total * 20 + digit``. Both standard and alternate glyph
        forms are accepted.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Medefaidrin._from_numeral('\U00016e80')
            0
            >>> Medefaidrin._from_numeral('\U00016e81')
            1
            >>> Medefaidrin._from_numeral('\U00016e93')
            19
            >>> Medefaidrin._from_numeral('\U00016e81\U00016e80')
            20
            >>> Medefaidrin._from_numeral('\U00016e82\U00016e82')
            42
            >>> Medefaidrin._from_numeral('\U00016e81\U00016e80\U00016e80')
            400
            >>> Medefaidrin._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Medefaidrin character: '?'
        """
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid Medefaidrin character: {char!r}")
            total = total * 20 + cls._from_numeral_map[char]
        return total
