"""Mayan numeral system converter.

This module implements the Mayan vigesimal (base-20) numeral system using
Unicode block U+1D2E0-U+1D2F3. Each of the 20 unique glyphs represents a
digit (0-19); numbers are encoded positionally, most-significant digit first,
analogous to the top-to-bottom writing direction of original Mayan inscriptions.

Unicode glyphs:

    𝋠  U+1D2E0  MAYAN NUMERAL ZERO       ->  0
    𝋡  U+1D2E1  MAYAN NUMERAL ONE        ->  1
    ...
    𝋳  U+1D2F3  MAYAN NUMERAL NINETEEN   ->  19

Examples of positional encoding (base 20):

    20   ->  𝋡𝋠   (1×20 + 0)
    399  ->  𝋳𝋳   (19×20 + 19)
    400  ->  𝋡𝋠𝋠  (1×400 + 0×20 + 0)
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System


class Mayan(System[str, int]):
    """Mayan vigesimal (base-20) numeral system converter.

    Implements bidirectional conversion between non-negative integers and Mayan
    numeral strings. Each character encodes a single vigesimal digit (0-19);
    digits are written most-significant first.

    The system includes zero (𝋠) and has no natural upper bound, so the valid
    range is 0 to infinity.

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (infinity).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    # Ordered list of digit glyphs: index == digit value
    _digits: ClassVar[list[str]] = [chr(0x1D2E0 + i) for i in range(20)]

    _to_numeral_map: Mapping[int, str] = {i: chr(0x1D2E0 + i) for i in range(20)}
    _from_numeral_map: Mapping[str, int] = {chr(0x1D2E0 + i): i for i in range(20)}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert a non-negative integer to its Mayan numeral representation.

        Encodes ``number`` in base 20, emitting the most-significant vigesimal
        digit first. Zero is represented by the single glyph 𝋠.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Mayan._to_numeral(0)
            '𝋠'
            >>> Mayan._to_numeral(1)
            '𝋡'
            >>> Mayan._to_numeral(19)
            '𝋳'
            >>> Mayan._to_numeral(20)
            '𝋡𝋠'
            >>> Mayan._to_numeral(399)
            '𝋳𝋳'
            >>> Mayan._to_numeral(400)
            '𝋡𝋠𝋠'
            >>> Mayan._to_numeral(8000)
            '𝋡𝋠𝋠𝋠'
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
        """Convert a Mayan numeral string to its integer value.

        Scans each glyph left-to-right, accumulating ``total = total * 20 + digit``.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Mayan._from_numeral('𝋠')
            0
            >>> Mayan._from_numeral('𝋳')
            19
            >>> Mayan._from_numeral('𝋡𝋠')
            20
            >>> Mayan._from_numeral('𝋳𝋳')
            399
            >>> Mayan._from_numeral('𝋡𝋠𝋠')
            400
            >>> Mayan._from_numeral('𝋡𝋠𝋠𝋠')
            8000
            >>> Mayan._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Mayan character: '?'
        """
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid {cls.__name__} character: {char!r}")
            total = total * 20 + cls._from_numeral_map[char]
        return total
