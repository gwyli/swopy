"""Greek Milesian numeral system conversion module.

This module provides conversion utilities for Greek Milesian (alphabetic) numerals.
It implements bidirectional conversion between Arabic numbers and Greek numerals.

Unicode glyphs used:
    Units (1–9):    α β γ δ ε ϛ ζ η θ
    Tens (10–90):   ι κ λ μ ν ξ ο π ϙ
    Hundreds (100–900): ρ σ τ υ φ χ ψ ω ϡ
    Thousands (1000–9000): ͵ (U+0375) prefix before the corresponding unit letter

The valid range is 1–9999.
"""

# Ignore ambiguous unicode character strings in Etruscan numerals
# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System


class Milesian(System[str, int]):
    """Greek Milesian (alphabetic) numeral system converter.

    Implements bidirectional conversion between integers and Greek Milesian
    numeral strings. The Milesian system is purely additive: each letter
    contributes its face value, and numerals are written largest-to-smallest.

    Thousands are denoted by the Greek numeral sign ͵ (U+0375) placed before
    the corresponding unit letter (e.g. ͵α = 1000, ͵θ = 9000).

    Attributes:
        _to_numeral_map: Ordered mapping of integer values to their Greek letter
            representations, from 9000 down to 1.
        _from_numeral_map: Mapping of Greek letter strings to their integer
            values. Thousands entries (two-character) are listed first so that
            longest-match iteration resolves ͵α before α.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Greek letters have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        9000: "\u0375\u03b8",  # ͵θ
        8000: "\u0375\u03b7",  # ͵η
        7000: "\u0375\u03b6",  # ͵ζ
        6000: "\u0375\u03db",  # ͵ϛ
        5000: "\u0375\u03b5",  # ͵ε
        4000: "\u0375\u03b4",  # ͵δ
        3000: "\u0375\u03b3",  # ͵γ
        2000: "\u0375\u03b2",  # ͵β
        1000: "\u0375\u03b1",  # ͵α
        900: "\u03e1",  # ϡ  sampi
        800: "\u03c9",  # ω
        700: "\u03c8",  # ψ
        600: "\u03c7",  # χ
        500: "\u03c6",  # φ
        400: "\u03c5",  # υ
        300: "\u03c4",  # τ
        200: "\u03c3",  # σ
        100: "\u03c1",  # ρ
        90: "\u03d9",  # ϙ  koppa
        80: "\u03c0",  # π
        70: "\u03bf",  # ο
        60: "\u03be",  # ξ
        50: "\u03bd",  # ν
        40: "\u03bc",  # μ
        30: "\u03bb",  # λ
        20: "\u03ba",  # κ
        10: "\u03b9",  # ι
        9: "\u03b8",  # θ
        8: "\u03b7",  # η
        7: "\u03b6",  # ζ
        6: "\u03db",  # ϛ  stigma
        5: "\u03b5",  # ε
        4: "\u03b4",  # δ
        3: "\u03b3",  # γ
        2: "\u03b2",  # β
        1: "\u03b1",  # α
    }

    # Both uppercase and lowercase entries are included so that either form is
    # accepted as input. Two-character thousands tokens must precede their
    # constituent single-character entries so that longest-match resolves
    # ͵Α/͵α as 1000 rather than ͵ (invalid) + Α/α (1).
    _from_numeral_map: Mapping[str, int] = {
        "\u0375\u0391": 1000,  # ͵Α
        "\u0375\u03b1": 1000,  # ͵α
        "\u0375\u0392": 2000,  # ͵Β
        "\u0375\u03b2": 2000,  # ͵β
        "\u0375\u0393": 3000,  # ͵Γ
        "\u0375\u03b3": 3000,  # ͵γ
        "\u0375\u0394": 4000,  # ͵Δ
        "\u0375\u03b4": 4000,  # ͵δ
        "\u0375\u0395": 5000,  # ͵Ε
        "\u0375\u03b5": 5000,  # ͵ε
        "\u0375\u03da": 6000,  # ͵Ϛ
        "\u0375\u03db": 6000,  # ͵ϛ
        "\u0375\u0396": 7000,  # ͵Ζ
        "\u0375\u03b6": 7000,  # ͵ζ
        "\u0375\u0397": 8000,  # ͵Η
        "\u0375\u03b7": 8000,  # ͵η
        "\u0375\u0398": 9000,  # ͵Θ
        "\u0375\u03b8": 9000,  # ͵θ
        "\u0391": 1,  # Α
        "\u03b1": 1,  # α
        "\u0392": 2,  # Β
        "\u03b2": 2,  # β
        "\u0393": 3,  # Γ
        "\u03b3": 3,  # γ
        "\u0394": 4,  # Δ
        "\u03b4": 4,  # δ
        "\u0395": 5,  # Ε
        "\u03b5": 5,  # ε
        "\u03da": 6,  # Ϛ
        "\u03db": 6,  # ϛ
        "\u0396": 7,  # Ζ
        "\u03b6": 7,  # ζ
        "\u0397": 8,  # Η
        "\u03b7": 8,  # η
        "\u0398": 9,  # Θ
        "\u03b8": 9,  # θ
        "\u0399": 10,  # Ι
        "\u03b9": 10,  # ι
        "\u039a": 20,  # Κ
        "\u03ba": 20,  # κ
        "\u039b": 30,  # Λ
        "\u03bb": 30,  # λ
        "\u039c": 40,  # Μ
        "\u03bc": 40,  # μ
        "\u039d": 50,  # Ν
        "\u03bd": 50,  # ν
        "\u039e": 60,  # Ξ
        "\u03be": 60,  # ξ
        "\u039f": 70,  # Ο
        "\u03bf": 70,  # ο
        "\u03a0": 80,  # Π
        "\u03c0": 80,  # π
        "\u03d8": 90,  # Ϙ
        "\u03d9": 90,  # ϙ
        "\u03a1": 100,  # Ρ
        "\u03c1": 100,  # ρ
        "\u03a3": 200,  # Σ
        "\u03c3": 200,  # σ
        "\u03a4": 300,  # Τ
        "\u03c4": 300,  # τ
        "\u03a5": 400,  # Υ
        "\u03c5": 400,  # υ
        "\u03a6": 500,  # Φ
        "\u03c6": 500,  # φ
        "\u03a7": 600,  # Χ
        "\u03c7": 600,  # χ
        "\u03a8": 700,  # Ψ
        "\u03c8": 700,  # ψ
        "\u03a9": 800,  # Ω
        "\u03c9": 800,  # ω
        "\u03e0": 900,  # Ϡ
        "\u03e1": 900,  # ϡ
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Greek Milesian representation.

        Uses greedy decomposition: at each step the largest denomination not
        exceeding the remainder is consumed, producing numerals in
        largest-to-smallest order.

        Args:
            number: The Arabic number to convert.

        Returns:
            The Greek Milesian string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Milesian._to_numeral(1)
            'α'
            >>> Milesian._to_numeral(9)
            'θ'
            >>> Milesian._to_numeral(10)
            'ι'
            >>> Milesian._to_numeral(11)
            'ια'
            >>> Milesian._to_numeral(999)
            'ϡϙθ'
            >>> Milesian._to_numeral(1000)
            '͵α'
            >>> Milesian._to_numeral(9999)
            '͵θϡϙθ'
        """
        result: str = ""

        for value, glyph in cls._to_numeral_map.items():
            count, number = divmod(number, value)
            result += glyph * count

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Greek Milesian numeral string to its Arabic integer value.

        Scans left-to-right using longest-match: two-character thousands tokens
        (e.g. ``͵α``) are tested before single-character tokens so that the
        Greek numeral sign ͵ is never left unmatched.

        Args:
            numeral: The Greek Milesian numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character or
                sequence.

        Examples:
            >>> Milesian._from_numeral('α')
            1
            >>> Milesian._from_numeral('ια')
            11
            >>> Milesian._from_numeral('ϡϙθ')
            999
            >>> Milesian._from_numeral('͵α')
            1000
            >>> Milesian._from_numeral('͵θϡϙθ')
            9999
        """
        total: int = 0
        i: int = 0

        while i < len(numeral):
            matched = False

            for symbol, value in cls._from_numeral_map.items():
                if numeral.startswith(symbol, i):
                    total += value
                    i += len(symbol)
                    matched = True
                    break

            if not matched:
                raise ValueError(
                    f"Invalid Greek Milesian character at position {i}: {numeral[i]!r}"
                )

        return total
