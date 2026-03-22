"""Brahmi-Dravidian script family numeral system converters.

This module implements numeral systems from scripts derived from Brahmi and
used in Dravidian-language contexts.

Currently supports:

    Grantha         U+11300-U+1137F
    Saurashtra      U+A880-U+A8DF
    Tamil           U+0B80-U+0BFF

Grantha uses seven combining digit marks (Unicode category Mn) for values 0-6,
encoded here as a positional base-7 system. Each digit position represents a
power of 7. Note: these are technically non-spacing combining marks in Unicode
and require a base character to render correctly; the glyphs are used as
standalone positional symbols in this implementation.

Saurashtra uses ten positional decimal digit glyphs (0-9) identical in
structure to the Arabic base-10 system. Numbers are encoded as a sequence of
digit glyphs representing the decimal expansion, most-significant digit first.

Tamil traditional numerals are a multiplicative-additive system.  Digit glyphs
(1-9) combine with multiplier signs (10, 100, 1000) by prefix: the digit
coefficient is written before the multiplier and omitted when equal to 1.
Ones are written using the digit glyphs directly; there are no dedicated
decade signs, so 20 is encoded as ௨௰ (digit 2 + ten sign).  The valid range
is 1-9999.
"""

# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import positional_from_numeral, positional_to_numeral


class Grantha(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and
    Grantha numerals.

    - Uses Unicode block U+11300-U+1137F, the seven combining digit glyphs
    - The system is positional in base 7, with the most-significant digit written
        first (left-to-right).

    Note: the Grantha digit characters are Unicode combining marks (category
    Mn). Standalone rendering may require a dotted circle base character.

    Attributes:
        minimum: Minimum valid value (0)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False, no value exists above infinity
        encodings: UTF-8
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x11366 + i) for i in range(7)}

    _from_numeral_map: Mapping[str, int] = {chr(0x11366 + i): i for i in range(7)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to its Grantha base-7 representation.

        Encodes ``denotation`` in base 7, emitting the most-significant digit
        first. Zero is represented by the single combining digit zero glyph.

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
        return positional_to_numeral(denotation, cls._to_numeral_map, 7)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Grantha base-7 numeral to its integer value.

        Scans each glyph left-to-right, accumulating
        ``total = total * 7 + digit``.

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
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 7)


class Saurashtra(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and
    Saurashtra numerals

    - Uses Unicode block U+A880-U+A8DF
    - The system is positional in base 10, using ten digit glyphs (0-9) at
        U+A8D0-U+A8D9
    - Denotations are encoded as a sequence of digit glyphs representing the decimal
        expansion, most-significant digit first (left-to-right).

    Attributes:
        minimum: Minimum valid value (0)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False, no values above infinity exist
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0xA8D0 + i) for i in range(10)}

    _from_numeral_map: Mapping[str, int] = {chr(0xA8D0 + i): i for i in range(10)}

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to Saurashtra numerals.

        Encodes ``denotation`` as a sequence of Saurashtra digit glyphs representing
        its decimal expansion, most-significant digit first. Zero is represented
        by the single zero glyph.

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
        return positional_to_numeral(denotation, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Saurashtra numeral to its integer value.

        Scans each glyph left-to-right, accumulating
        ``total = total * 10 + digit``.

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
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 10)


class Tamil(System[str, int]):
    """Implements bidirectional conversion between integers and Tamil traditional
    numeral strings.

    - Uses Unicode block U+0B80-U+0BFF
    - The system is multiplicative-additive: digit glyphs (1-9) precede a multiplier
     sign (10, 100, 1000); the digit is omitted when the coefficient is 1
    - There are no dedicated decade signs, so 20 is ௨௰ (digit 2 + ten sign)

    Distinct from Tamil decimal digits (U+0BE6-U+0BEF), which form a
    Hindu-Arabic positional system; these traditional forms use the
    higher-order signs U+0BF0-U+0BF2 as multipliers.

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (9999)
        maximum_is_many: False, integers above 9999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    # Digit glyphs 1-9 (U+0BE7-U+0BEF)
    _digit_map: ClassVar[Mapping[int, str]] = {i: chr(0x0BE6 + i) for i in range(1, 10)}

    # Multiplier glyphs (largest first for greedy decomposition)
    _multiplier_map: ClassVar[Mapping[int, str]] = {
        1000: "\u0bf2",  # ௲  TAMIL NUMBER ONE THOUSAND
        100: "\u0bf1",  # ௱  TAMIL NUMBER ONE HUNDRED
        10: "\u0bf0",  # ௰  TAMIL NUMBER TEN
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    _to_numeral_map: Mapping[int, str] = {**_digit_map}

    # Digit-only reverse map (1-9); used internally as coefficient lookup.
    _digit_from_map: ClassVar[Mapping[str, int]] = {v: k for k, v in _digit_map.items()}

    # Full from_numeral_map includes both digit glyphs and multiplier signs so
    # that standalone multiplier inputs are recognised as valid characters.
    _from_numeral_map: Mapping[str, int] = {
        **{v: k for k, v in _digit_map.items()},
        "\u0bf0": 10,  # ௰  TAMIL NUMBER TEN
        "\u0bf1": 100,  # ௱  TAMIL NUMBER ONE HUNDRED
        "\u0bf2": 1000,  # ௲  TAMIL NUMBER ONE THOUSAND
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an integer to a Tamil traditional numeral.

        The digit coefficient is omitted when equal to 1; ones use the digit
        glyphs directly; no dedicated decade signs exist.

        Examples:
            >>> Tamil._to_numeral(1)
            '௧'
            >>> Tamil._to_numeral(10)
            '௰'
            >>> Tamil._to_numeral(20)
            '௨௰'
            >>> Tamil._to_numeral(100)
            '௱'
            >>> Tamil._to_numeral(200)
            '௨௱'
            >>> Tamil._to_numeral(1000)
            '௲'
            >>> Tamil._to_numeral(1996)
            '௲௯௱௯௰௬'
        """
        result = ""
        for mult in [1000, 100, 10]:
            coeff = denotation // mult
            denotation = denotation % mult
            if coeff:
                if coeff > 1:
                    result += cls._digit_map[coeff]
                result += cls._multiplier_map[mult]
        if denotation:
            result += cls._digit_map[denotation]
        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Tamil traditional numeral to an integer.

        Scans left-to-right.  A digit glyph immediately followed by a
        multiplier sign contributes ``digit × multiplier``; a lone multiplier
        sign contributes ``1 × multiplier``; a lone digit contributes its
        face value.

        Examples:
            >>> Tamil._from_numeral('௧')
            1
            >>> Tamil._from_numeral('௰')
            10
            >>> Tamil._from_numeral('௨௰')
            20
            >>> Tamil._from_numeral('௱')
            100
            >>> Tamil._from_numeral('௨௱')
            200
            >>> Tamil._from_numeral('௲')
            1000
            >>> Tamil._from_numeral('௲௯௱௯௰௬')
            1996
            >>> Tamil._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Tamil character: '?'
        """
        total = 0
        i = 0
        while i < len(numeral):
            c = numeral[i]
            if c in cls._digit_from_map:
                # Digit glyph (1-9): may be followed by a multiplier
                digit = cls._digit_from_map[c]
                i += 1
                if i < len(numeral) and numeral[i] in cls._multiplier_from_map:
                    total += digit * cls._multiplier_from_map[numeral[i]]
                    i += 1
                else:
                    total += digit
            elif c in cls._multiplier_from_map:
                # Standalone multiplier: implicit coefficient of 1
                total += cls._multiplier_from_map[c]
                i += 1
            else:
                raise ValueError(f"Invalid Tamil character: {c!r}")
        return total
