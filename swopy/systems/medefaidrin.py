"""Medefaidrin numeral system converters.

This module implements numeral systems from the Medefaidrin script family,
used in Nigeria.
Currently supports:

    Medefaidrin  U+16E40-U+16E9F

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
from ._algorithms import positional_from_numeral, positional_to_numeral


class Medefaidrin(System[str, int]):
    """Implements bidirectional conversion between non-negative integers and
    Medefaidrin numerals.

    - Uses Unicode block U+16E80-U+16E93 (digits 0-19) within block U+16E40-U+16E9F
    - The system is positional in base 20, using twenty unique digit glyphs (0-19)
    - Numbers are written most-significant digit first (left-to-right)
    - Alternate forms for 1, 2, and 3 (U+16E94-U+16E96) are accepted as input
      but not emitted

    Attributes:
        minimum: Minimum valid value (0)
        maximum: Maximum valid value (+infinity)
        maximum_is_many: False - no natural bound exists
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {i: chr(0x16E80 + i) for i in range(20)}

    _from_numeral_map: Mapping[str, int] = {
        **{chr(0x16E80 + i): i for i in range(20)},
        "\U00016e94": 1,  # 𛺔 MEDEFAIDRIN DIGIT ONE ALTERNATE FORM
        "\U00016e95": 2,  # 𛺕 MEDEFAIDRIN DIGIT TWO ALTERNATE FORM
        "\U00016e96": 3,  # 𛺖 MEDEFAIDRIN DIGIT THREE ALTERNATE FORM
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert a non-negative integer to its Medefaidrin base-20 representation.

        Encodes ``denotation`` in base 20, emitting the most-significant vigesimal
        digit first. Zero is represented by the single glyph 𛺀.

        Args:
            denotation: The non-negative integer to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

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
        return positional_to_numeral(denotation, cls._to_numeral_map, 20)

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
        return positional_from_numeral(numeral, cls._from_numeral_map, cls.__name__, 20)
