"""Brahmi-Tai script family numeral system converters.

This module implements numeral systems from scripts derived from Brahmi and
used in Tai-language contexts.
Currently supports:

    Ahom  U+11700-U+1174F  (ten positional digit glyphs: 0-9, U+11730-U+11739)

Ahom uses ten positional decimal digit glyphs (0-9) identical in structure to
the Arabic base-10 system. Numbers are encoded as a sequence of digit glyphs
representing the decimal expansion, most-significant digit first. The block
also contains dedicated signs for ten (U+1173A) and twenty (U+1173B) used in
manuscript contexts; these are accepted as input but the positional decimal
encoding is used for output.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import positional_to_numeral


class Ahom(System[str, int]):
    """Ahom decimal numeral system converter.

    Implements bidirectional conversion between non-negative integers and Ahom
    numeral strings using Unicode block U+11700-U+1174F. The system is
    positional in base 10, using ten digit glyphs (0-9) at U+11730-U+11739.
    Numbers are encoded as a sequence of digit glyphs representing the decimal
    expansion, most-significant digit first (left-to-right).

    The dedicated ten (U+1173A) and twenty (U+1173B) signs are accepted as
    input (decoding to 10 and 20 respectively) but are not emitted on output.

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (+infinity).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x11730 + i) for i in range(10)}

    _from_numeral_map: Mapping[str, int] = {
        **{chr(0x11730 + i): i for i in range(10)},
        "\U0001173a": 10,  # 𑜺 AHOM NUMBER TEN
        "\U0001173b": 20,  # 𑜻 AHOM NUMBER TWENTY
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to its Ahom decimal representation.

        Encodes ``denotation`` as a sequence of Ahom digit glyphs representing its
        decimal expansion, most-significant digit first. Zero is represented
        by the single zero glyph.

        Args:
            denotation: The non-negative integer to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Ahom._to_numeral(0)
            '\U00011730'
            >>> Ahom._to_numeral(1)
            '\U00011731'
            >>> Ahom._to_numeral(9)
            '\U00011739'
            >>> Ahom._to_numeral(10)
            '\U00011731\U00011730'
            >>> Ahom._to_numeral(42)
            '\U00011734\U00011732'
            >>> Ahom._to_numeral(100)
            '\U00011731\U00011730\U00011730'
        """
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ahom numeral string to its integer value.

        Scans each character left-to-right. Positional digit glyphs (U+11730-
        U+11739) accumulate using ``total = total * 10 + digit``. The dedicated
        ten (U+1173A) and twenty (U+1173B) signs are treated as additive
        contributions of 10 and 20.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Ahom._from_numeral('\U00011730')
            0
            >>> Ahom._from_numeral('\U00011731')
            1
            >>> Ahom._from_numeral('\U00011739')
            9
            >>> Ahom._from_numeral('\U00011731\U00011730')
            10
            >>> Ahom._from_numeral('\U00011734\U00011732')
            42
            >>> Ahom._from_numeral('\U0001173a')
            10
            >>> Ahom._from_numeral('\U0001173b')
            20
            >>> Ahom._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Ahom character: '?'
        """
        _digit_base = 0x11730
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid Ahom character: {char!r}")
            cp = ord(char)
            if _digit_base <= cp <= _digit_base + 9:
                total = total * 10 + (cp - _digit_base)
            else:
                total += cls._from_numeral_map[char]
        return total
