"""Kaktovik (Iñupiaq) numeral system converters.

This module implements numeral systems from the Inuit cultural sphere.
Currently supports:

    Kaktovik  U+1D2C0-U+1D2DF  (twenty digits: zero through nineteen)

Kaktovik is a positional base-20 (vigesimal) system, analogous to the
Arabic base-10 system.  Each digit position is a power of 20; the twenty
unique glyphs encode the values 0-19.  Numbers are written most-significant
digit first, matching the left-to-right convention.

Negative numbers are prefixed with a hyphen-minus (U+002D).
"""

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import positional_from_numeral, positional_to_numeral


class Kaktovik(System[str, int]):
    """Implements bidirectional conversion between integers and Kaktovik numerals.

    - Uses Unicode block U+1D2C0-U+1D2DF
    - The system is positional in base 20, using twenty unique digit glyphs (0-19)
    - Negative numbers are prefixed with a hyphen-minus (U+002D)

    Attributes:
        minimum: Minimum valid value (-infinity)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False - no natural bound exists
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = -inf
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x1D2C0 + i) for i in range(20)}

    _from_numeral_map: Mapping[str, int] = {chr(0x1D2C0 + i): i for i in range(20)}

    @classmethod
    def from_numeral_map(cls) -> Mapping[str, int]:
        """Returns all valid Kaktovik characters mapped to their digit values.

        Combines the twenty digit glyphs (0-19) with the hyphen-minus sign
        used to denote negative numbers, so callers see the complete set of
        accepted input characters.

        Returns:
            A mapping from every valid Kaktovik character to its digit value.
        """
        return {**cls._from_numeral_map, "-": 0}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to its Kaktovik numeral representation.

        Encodes ``denotation`` in base 20, emitting the most-significant vigesimal
        digit first.  Negative denotations are prefixed with a hyphen-minus.
        Zero is represented by the single glyph 𝋀.

        Args:
            denotation: The integer to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> Kaktovik._to_numeral(0)
            '𝋀'
            >>> Kaktovik._to_numeral(1)
            '𝋁'
            >>> Kaktovik._to_numeral(19)
            '𝋓'
            >>> Kaktovik._to_numeral(20)
            '𝋁𝋀'
            >>> Kaktovik._to_numeral(42)
            '𝋂𝋂'
            >>> Kaktovik._to_numeral(400)
            '𝋁𝋀𝋀'
            >>> Kaktovik._to_numeral(-1)
            '-𝋁'
            >>> Kaktovik._to_numeral(-42)
            '-𝋂𝋂'
        """
        if denotation < 0:
            return "-" + positional_to_numeral(-denotation, cls._to_numeral_map, 20)
        return positional_to_numeral(denotation, cls._to_numeral_map, 20)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Kaktovik numeral string to its integer value.

        Scans each glyph left-to-right, accumulating ``total = total * 20 + digit``.
        A leading hyphen-minus negates the result.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Kaktovik._from_numeral('𝋀')
            0
            >>> Kaktovik._from_numeral('𝋁')
            1
            >>> Kaktovik._from_numeral('𝋓')
            19
            >>> Kaktovik._from_numeral('𝋁𝋀')
            20
            >>> Kaktovik._from_numeral('𝋂𝋂')
            42
            >>> Kaktovik._from_numeral('𝋁𝋀𝋀')
            400
            >>> Kaktovik._from_numeral('-𝋁')
            -1
            >>> Kaktovik._from_numeral('-𝋂𝋂')
            -42
            >>> Kaktovik._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Kaktovik character: '?'
            >>> Kaktovik._from_numeral('-')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Kaktovik numeral: '-'
        """
        negative = numeral.startswith("-")
        digits = numeral[1:] if negative else numeral
        if not digits:
            raise ValueError(f"Invalid Kaktovik numeral: {numeral!r}")
        total = positional_from_numeral(digits, cls._from_numeral_map, cls.__name__, 20)
        return -total if negative else total
