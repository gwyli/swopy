"""Sino-Tibetan numeral system converters.

This module implements numeral systems from the Sino-Tibetan script family.
Currently supports:

    Tangut        U+17000-U+187FF  (specific glyphs listed below)
    Khitan Small  U+18B00-U+18CFF  (specific glyphs listed below)
    Suzhou        U+3000-U+303F    (Hangzhou numerals; digits U+3021-U+3029,
                                    zero U+3007; shorthand U+3038-U+303A)
    Chinese       U+4E00-U+9FFF    (CJK ideographic numerals; digits
                                    一-九, multipliers 十/百/千/万)

Tangut and Khitan are multiplicative-additive with myriad (10,000) grouping.
Digits 1-9 have unique glyphs; multipliers for 10, 100, 1,000 and 10,000
are separate characters.  Zero is omitted from normal use (place values are
simply skipped when their digit is zero).

Tangut: the tens place always carries an explicit digit (including 1);
other place digits default to omitting 1.

Khitan: digit 1 is omitted before every multiplier (including tens).

Suzhou (Huāmǎ / 花碼) is a positional decimal system derived from counting
rods.  Digits U+3021-U+3029 represent 1-9; U+3007 represents 0.  The
shorthand glyphs U+3038, U+3039, U+303A (values 10, 20, 30) are accepted
in decoding as standalone numerals but are not produced by encoding.

Chinese (CJK) is a multiplicative-additive myriad system.  Digit ideographs
一-九 combine with multiplier ideographs 十/百/千/万; the digit 一 is omitted
before every multiplier.  The zero character 零 is accepted in decoding as a
placeholder linker but contributes no value; it is not produced by encoding.
The valid range is 1-99,999,999.
"""

# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from math import inf
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_myriad_from_numeral,
    multiplicative_myriad_to_numeral,
    positional_to_numeral,
)


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

    # Multiplier glyphs (largest first)
    _multiplier_map: ClassVar[Mapping[int, str]] = {
        10000: "\U00017457",  # 𗑗  Tangut myriad (x10,000)
        1000: "\U000170d4",  # 𗃔  Tangut thousand (x1,000)
        100: "\U000172da",  # 𗋚  Tangut hundred (x100)
        10: "\U00017c17",  # 𗰗  Tangut ten (x10)
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    _myriad_sub_mult: ClassVar[tuple[tuple[int, str], ...]] = tuple(
        (k, v)
        for k, v in _multiplier_map.items()
        if k != 10000  # noqa: PLR2004
    )

    @classmethod
    def from_numeral_map(cls) -> Mapping[str, int]:
        """Returns all valid Tangut characters mapped to their numeric values.

        Combines digit glyphs (1-9) and multiplier glyphs (10, 100, 1000,
        10000) so that callers see the complete set of accepted characters.

        Returns:
            A mapping from every valid Tangut glyph to its numeric value.
        """
        return {**cls._from_numeral_map, **cls._multiplier_from_map}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Tangut numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + myriad``,
        where the coefficient (1-9999) is itself encoded as a sub-myriad number.
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
        return multiplicative_myriad_to_numeral(
            number,
            cls._to_numeral_map,
            cls._multiplier_map,
            explicit_one_tens=True,
            sub_mult=cls._myriad_sub_mult,
        )

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
        return multiplicative_myriad_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls._multiplier_from_map,
            cls.__name__,
        )


class Khitan(System[str, int]):
    """Khitan numeral system converter.

    Implements bidirectional conversion between integers and Khitan Small
    Script numeral strings. The system is multiplicative-additive with a
    myriad base:

    - Digits 1-9 are represented by unique glyphs (U+18B00-U+18B08).
    - Multipliers x10, x100, x1000, x10000 are separate characters.
    - The digit 1 is always omitted before every multiplier (including tens).
    - Zero places are skipped entirely (no zero glyph in normal use).
    - The myriad (x10000) coefficient can itself be a sub-myriad number
      (2-9999); a coefficient of 1 is omitted entirely.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999,999).
        encodings: UTF-8 only, as no ASCII equivalents exist.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999

    encodings: ClassVar[Encodings] = {"utf8"}

    # Individual digit glyphs (1-9): U+18B00-U+18B08
    _to_numeral_map: Mapping[int, str] = {i: chr(0x18B00 + i - 1) for i in range(1, 10)}

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    # Multiplier glyphs (largest first)
    _multiplier_map: ClassVar[Mapping[int, str]] = {
        10000: "\U00018b0c",  # Khitan myriad (x10,000)
        1000: "\U00018b0b",  # Khitan thousand (x1,000)
        100: "\U00018b09",  # Khitan hundred (x100)
        10: "\U00018b0a",  # Khitan ten (x10)
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    _myriad_sub_mult: ClassVar[tuple[tuple[int, str], ...]] = tuple(
        (k, v)
        for k, v in _multiplier_map.items()
        if k != 10000  # noqa: PLR2004
    )

    @classmethod
    def from_numeral_map(cls) -> Mapping[str, int]:
        """Returns all valid Khitan characters mapped to their numeric values.

        Combines digit glyphs (1-9) and multiplier glyphs (10, 100, 1000,
        10000) so that callers see the complete set of accepted characters.

        Returns:
            A mapping from every valid Khitan glyph to its numeric value.
        """
        return {**cls._from_numeral_map, **cls._multiplier_from_map}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Khitan numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + myriad``,
        where a coefficient of 1 is omitted and coefficients 2-9999 are
        encoded as sub-myriad numbers. The remainder (0-9999) is appended
        directly.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Khitan._to_numeral(1)
            '\U00018b00'
            >>> Khitan._to_numeral(10)
            '\U00018b0a'
            >>> Khitan._to_numeral(12)
            '\U00018b0a\U00018b01'
            >>> Khitan._to_numeral(100)
            '\U00018b09'
            >>> Khitan._to_numeral(10000)
            '\U00018b0c'
            >>> Khitan._to_numeral(100000)
            '\U00018b0a\U00018b0c'
            >>> Khitan._to_numeral(20000)
            '\U00018b01\U00018b0c'
        """
        return multiplicative_myriad_to_numeral(
            number,
            cls._to_numeral_map,
            cls._multiplier_map,
            explicit_one_tens=False,
            sub_mult=cls._myriad_sub_mult,
        )

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Khitan numeral string to its Arabic integer value.

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
            >>> Khitan._from_numeral('\U00018b00')
            1
            >>> Khitan._from_numeral('\U00018b0a')
            10
            >>> Khitan._from_numeral('\U00018b0a\U00018b01')
            12
            >>> Khitan._from_numeral('\U00018b09')
            100
            >>> Khitan._from_numeral('\U00018b0c')
            10000
            >>> Khitan._from_numeral('\U00018b0a\U00018b0c')
            100000
            >>> Khitan._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Khitan character: '?'
        """
        return multiplicative_myriad_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls._multiplier_from_map,
            cls.__name__,
        )


class Suzhou(System[str, int]):
    """Suzhou (Huāmǎ / 花碼) numeral system converter.

    Implements bidirectional conversion between non-negative integers and
    Suzhou numeral strings using Unicode block U+3000-U+303F.  The system is
    positional base-10: digit glyphs U+3021-U+3029 represent 1-9 and U+3007
    represents 0.  The shorthand glyphs U+3038 (ten), U+3039 (twenty), and
    U+303A (thirty) are accepted as standalone numerals in decoding but are
    never produced by encoding.

    Attributes:
        minimum: Minimum valid value (0).
        maximum: Maximum valid value (+infinity).
        encodings: UTF-8 only; glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 0
    maximum: ClassVar[int | float | Fraction] = inf

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        0: "\u3007",  # 〇 IDEOGRAPHIC NUMBER ZERO
        **{i: chr(0x3020 + i) for i in range(1, 10)},
    }

    _from_numeral_map: Mapping[str, int] = {
        "\u3007": 0,  # 〇 zero
        **{chr(0x3020 + i): i for i in range(1, 10)},
        "\u3038": 10,  # 〸 HANGZHOU NUMERAL TEN   (shorthand, decode only)
        "\u3039": 20,  # 〹 HANGZHOU NUMERAL TWENTY (shorthand, decode only)
        "\u303a": 30,  # 〺 HANGZHOU NUMERAL THIRTY (shorthand, decode only)
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert a non-negative integer to its Suzhou positional representation.

        Encodes ``number`` as a sequence of Hangzhou numeral glyphs
        representing its decimal expansion, most-significant digit first.
        Zero is represented by the single ideographic zero glyph U+3007.

        Args:
            number: The non-negative integer to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Suzhou._to_numeral(0)
            '〇'
            >>> Suzhou._to_numeral(1)
            '〡'
            >>> Suzhou._to_numeral(9)
            '〩'
            >>> Suzhou._to_numeral(10)
            '〡〇'
            >>> Suzhou._to_numeral(42)
            '〤〢'
            >>> Suzhou._to_numeral(100)
            '〡〇〇'
        """
        return positional_to_numeral(number, cls._to_numeral_map, 10)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Suzhou numeral string to its Arabic integer value.

        Standalone shorthand glyphs U+3038-U+303A decode to 10, 20, 30
        respectively.  All other strings are decoded positionally.

        Args:
            numeral: The numeral string to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Suzhou._from_numeral('〇')
            0
            >>> Suzhou._from_numeral('〡')
            1
            >>> Suzhou._from_numeral('〡〇')
            10
            >>> Suzhou._from_numeral('〸')
            10
            >>> Suzhou._from_numeral('〤〢')
            42
            >>> Suzhou._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Suzhou character: '?'
        """
        total = 0
        for char in numeral:
            if char not in cls._from_numeral_map:
                raise ValueError(f"Invalid Suzhou character: {char!r}")
            value = cls._from_numeral_map[char]
            # Detect shorthand numerals and prevent their use mid-string
            if value >= 10:  # noqa: PLR2004
                if len(numeral) != 1:
                    raise ValueError(f"Invalid Suzhou character: {char!r}")
                return value
            total = total * 10 + value
        return total


class Chinese(System[str, int]):
    """Chinese (CJK) numeral system converter.

    Implements bidirectional conversion between integers and Chinese numeral
    strings using CJK Unified Ideographs (U+4E00-U+9FFF).  The system is
    multiplicative-additive with myriad (10,000) grouping: digit ideographs
    一-九 combine with multiplier ideographs 十/百/千/万.  The digit 一 is
    omitted before every multiplier (including 十).  The zero character 零
    is accepted as a placeholder in decoding but contributes no value and
    is not produced by encoding.  The valid range is 1-99,999,999.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99,999,999).
        encodings: UTF-8 only; glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99_999_999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1: "\u4e00",  # 一
        2: "\u4e8c",  # 二
        3: "\u4e09",  # 三
        4: "\u56db",  # 四
        5: "\u4e94",  # 五
        6: "\u516d",  # 六
        7: "\u4e03",  # 七
        8: "\u516b",  # 八
        9: "\u4e5d",  # 九
    }

    _from_numeral_map: Mapping[str, int] = {
        **{v: k for k, v in _to_numeral_map.items()},
        "\u96f6": 0,  # 零 zero linker (ignored in decoding)
    }

    _multiplier_map: ClassVar[Mapping[int, str]] = {
        10000: "\u4e07",  # 万
        1000: "\u5343",  # 千
        100: "\u767e",  # 百
        10: "\u5341",  # 十
    }

    _multiplier_from_map: ClassVar[Mapping[str, int]] = {
        v: k for k, v in _multiplier_map.items()
    }

    _myriad_sub_mult: ClassVar[tuple[tuple[int, str], ...]] = tuple(
        (k, v)
        for k, v in _multiplier_map.items()
        if k != 10000  # noqa: PLR2004
    )

    @classmethod
    def from_numeral_map(cls) -> Mapping[str, int]:
        """Returns all valid Chinese characters mapped to their numeric values.

        Combines digit glyphs (一-九), the zero linker (零), and multiplier
        glyphs (十/百/千/万) so that callers see the complete set of accepted
        characters.

        Returns:
            A mapping from every valid Chinese glyph to its numeric value.
        """
        return {**cls._from_numeral_map, **cls._multiplier_from_map}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Chinese numeral representation.

        Numbers >= 10,000 are expressed as ``encode(coefficient) + 万``,
        where the coefficient (1-9999) is itself encoded as a sub-myriad
        number.  The digit 一 is omitted before every multiplier.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Chinese._to_numeral(1)
            '一'
            >>> Chinese._to_numeral(10)
            '十'
            >>> Chinese._to_numeral(20)
            '二十'
            >>> Chinese._to_numeral(100)
            '百'
            >>> Chinese._to_numeral(1000)
            '千'
            >>> Chinese._to_numeral(10000)
            '万'
            >>> Chinese._to_numeral(20000)
            '二万'
            >>> Chinese._to_numeral(99999999)
            '九千九百九十九万九千九百九十九'
        """
        return multiplicative_myriad_to_numeral(
            number,
            cls._to_numeral_map,
            cls._multiplier_map,
            explicit_one_tens=False,
            sub_mult=cls._myriad_sub_mult,
        )

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Chinese numeral string to its Arabic integer value.

        Splits at the myriad glyph 万 (if present); the portion before it is
        parsed as a sub-myriad coefficient and multiplied by 10,000; the
        portion after is parsed as the remainder.  The zero character 零
        is accepted as a placeholder but contributes no value.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Chinese._from_numeral('一')
            1
            >>> Chinese._from_numeral('十')
            10
            >>> Chinese._from_numeral('二十')
            20
            >>> Chinese._from_numeral('百')
            100
            >>> Chinese._from_numeral('万')
            10000
            >>> Chinese._from_numeral('九千九百九十九万九千九百九十九')
            99999999
            >>> Chinese._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Chinese character: '?'
        """
        return multiplicative_myriad_from_numeral(
            numeral,
            cls._from_numeral_map,
            cls._multiplier_from_map,
            cls.__name__,
        )
