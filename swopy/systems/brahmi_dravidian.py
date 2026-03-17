"""Brahmi-Dravidian script family numeral system converters.

This module implements numeral systems from scripts derived from Brahmi and
used in Dravidian-language contexts.
Currently supports:

    Grantha    U+11300-U+1137F  (seven combining digit glyphs: 0-6,
                                  U+11366-U+1136C)
    Saurashtra U+A880-U+A8DF   (ten positional digit glyphs: 0-9,
                                  U+A8D0-U+A8D9)

Grantha uses seven combining digit marks (Unicode category Mn) for values 0-6,
encoded here as a positional base-7 system. Each digit position represents a
power of 7. Note: these are technically non-spacing combining marks in Unicode
and require a base character to render correctly; the glyphs are used as
standalone positional symbols in this implementation.

Saurashtra uses ten positional decimal digit glyphs (0-9) identical in
structure to the Arabic base-10 system. Numbers are encoded as a sequence of
digit glyphs representing the decimal expansion, most-significant digit first.
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System


class Grantha(System[str, int]):
    """Grantha base-7 numeral system converter.

    Implements bidirectional conversion between non-negative integers and
    Grantha numeral strings using the seven combining digit glyphs
    U+11366-U+1136C (values 0-6). The system is positional in base 7, with
    the most-significant digit written first (left-to-right).

    Note: the Grantha digit characters are Unicode combining marks (category
    Mn). Standalone rendering may require a dotted circle base character.

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (+infinity).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x11366 + i) for i in range(7)}

    _from_numeral_map: Mapping[str, int] = {chr(0x11366 + i): i for i in range(7)}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert a non-negative integer to its Grantha base-7 representation.

        Encodes ``number`` in base 7, emitting the most-significant digit
        first. Zero is represented by the single combining digit zero glyph.

        Args:
            number: The non-negative integer to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Grantha._to_numeral(0)
            '𑍦'
            >>> Grantha._to_numeral(1)
            '𑍧'
            >>> Grantha._to_numeral(6)
            '𑍬'
            >>> Grantha._to_numeral(7)
            '𑍧𑍦'
            >>> Grantha._to_numeral(49)
            '𑍧𑍦𑍦'
        """
        if number == 0:
            return cls._to_numeral_map[0]
        parts: list[str] = []
        while number:
            number, remainder = divmod(number, 7)
            parts.append(cls._to_numeral_map[remainder])
        return "".join(reversed(parts))

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Grantha base-7 numeral string to its integer value.

        Scans each glyph left-to-right, accumulating
        ``total = total * 7 + digit``.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Grantha._from_numeral('𑍦')
            0
            >>> Grantha._from_numeral('𑍧')
            1
            >>> Grantha._from_numeral('𑍬')
            6
            >>> Grantha._from_numeral('𑍧𑍦')
            7
            >>> Grantha._from_numeral('𑍧𑍦𑍦')
            49
            >>> Grantha._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Grantha character: '?'
        """
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid Grantha character: {char!r}")
            total = total * 7 + cls._from_numeral_map[char]
        return total


class Saurashtra(System[str, int]):
    """Saurashtra decimal numeral system converter.

    Implements bidirectional conversion between non-negative integers and
    Saurashtra numeral strings using Unicode block U+A880-U+A8DF. The system
    is positional in base 10, using ten digit glyphs (0-9) at U+A8D0-U+A8D9.
    Numbers are encoded as a sequence of digit glyphs representing the decimal
    expansion, most-significant digit first (left-to-right).

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (+infinity).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0xA8D0 + i) for i in range(10)}

    _from_numeral_map: Mapping[str, int] = {chr(0xA8D0 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert a non-negative integer to its Saurashtra decimal representation.

        Encodes ``number`` as a sequence of Saurashtra digit glyphs representing
        its decimal expansion, most-significant digit first. Zero is represented
        by the single zero glyph.

        Args:
            number: The non-negative integer to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Saurashtra._to_numeral(0)
            '\ua8d0'
            >>> Saurashtra._to_numeral(1)
            '\ua8d1'
            >>> Saurashtra._to_numeral(9)
            '\ua8d9'
            >>> Saurashtra._to_numeral(10)
            '\ua8d1\ua8d0'
            >>> Saurashtra._to_numeral(42)
            '\ua8d4\ua8d2'
            >>> Saurashtra._to_numeral(100)
            '\ua8d1\ua8d0\ua8d0'
        """
        if number == 0:
            return cls._to_numeral_map[0]
        parts: list[str] = []
        while number:
            number, remainder = divmod(number, 10)
            parts.append(cls._to_numeral_map[remainder])
        return "".join(reversed(parts))

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Saurashtra numeral string to its integer value.

        Scans each glyph left-to-right, accumulating
        ``total = total * 10 + digit``.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Saurashtra._from_numeral('\ua8d0')
            0
            >>> Saurashtra._from_numeral('\ua8d1')
            1
            >>> Saurashtra._from_numeral('\ua8d9')
            9
            >>> Saurashtra._from_numeral('\ua8d1\ua8d0')
            10
            >>> Saurashtra._from_numeral('\ua8d4\ua8d2')
            42
            >>> Saurashtra._from_numeral('\ua8d1\ua8d0\ua8d0')
            100
            >>> Saurashtra._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Saurashtra character: '?'
        """
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid Saurashtra character: {char!r}")
            total = total * 10 + cls._from_numeral_map[char]
        return total
