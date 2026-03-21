"""Siyaq numeral system converters.

This module implements numeral systems from the Siyaq accounting tradition,
used in Ottoman Turkish and Indo-Persian administrative contexts.
Currently supports:

    Ottoman Siyaq  U+1ED00-U+1ED4F  (forty-five standard glyphs covering 1-9,
                                      10-90, 100-900, 1000-9000, 10000-90000;
                                      plus alternate forms at U+1ED2F-U+1ED3B)
    Indic Siyaq    U+1EC70-U+1ECBF  (forty-five standard glyphs covering 1-9,
                                      10-90, 100-900, 1000-9000, 10000-90000;
                                      plus alternate and prefixed forms)

Both systems assign a unique glyph to each representable value (no repetition
of a single glyph). Both are written right-to-left (largest denomination on
the right). Encoding uses greedy decomposition followed by reversal; decoding
reverses the input before summing character values.
"""

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


class OttomanSiyaq(System[str, int]):
    """Implements bidirectional conversion between integers and Ottoman Siyaq numerals.

    - Uses Unicode block U+1ED00-U+1ED4F (forty-five standard glyphs: units 1-9, decades
      10-90, hundreds 100-900, thousands 1,000-9,000, ten-thousands 10,000-90,000;
      alternate forms at U+1ED2F-U+1ED3B accepted as input but not emitted)
    - The system is purely additive with one unique glyph per denomination; written
      right-to-left (largest denomination on the right)
    - Encoding reverses the greedy result; decoding reverses the input before summing

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (99,999)
        maximum_is_many: False - integers greater than 99,999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        90000: "\U0001ed2d",  # 𞴭 OTTOMAN SIYAQ NUMBER NINETY THOUSAND
        80000: "\U0001ed2c",  # 𞴬 OTTOMAN SIYAQ NUMBER EIGHTY THOUSAND
        70000: "\U0001ed2b",  # 𞴫 OTTOMAN SIYAQ NUMBER SEVENTY THOUSAND
        60000: "\U0001ed2a",  # 𞴪 OTTOMAN SIYAQ NUMBER SIXTY THOUSAND
        50000: "\U0001ed29",  # 𞴩 OTTOMAN SIYAQ NUMBER FIFTY THOUSAND
        40000: "\U0001ed28",  # 𞴨 OTTOMAN SIYAQ NUMBER FORTY THOUSAND
        30000: "\U0001ed27",  # 𞴧 OTTOMAN SIYAQ NUMBER THIRTY THOUSAND
        20000: "\U0001ed26",  # 𞴦 OTTOMAN SIYAQ NUMBER TWENTY THOUSAND
        10000: "\U0001ed25",  # 𞴥 OTTOMAN SIYAQ NUMBER TEN THOUSAND
        9000: "\U0001ed24",  # 𞴤 OTTOMAN SIYAQ NUMBER NINE THOUSAND
        8000: "\U0001ed23",  # 𞴣 OTTOMAN SIYAQ NUMBER EIGHT THOUSAND
        7000: "\U0001ed22",  # 𞴢 OTTOMAN SIYAQ NUMBER SEVEN THOUSAND
        6000: "\U0001ed21",  # 𞴡 OTTOMAN SIYAQ NUMBER SIX THOUSAND
        5000: "\U0001ed20",  # 𞴠 OTTOMAN SIYAQ NUMBER FIVE THOUSAND
        4000: "\U0001ed1f",  # 𞴟 OTTOMAN SIYAQ NUMBER FOUR THOUSAND
        3000: "\U0001ed1e",  # 𞴞 OTTOMAN SIYAQ NUMBER THREE THOUSAND
        2000: "\U0001ed1d",  # 𞴝 OTTOMAN SIYAQ NUMBER TWO THOUSAND
        1000: "\U0001ed1c",  # 𞴜 OTTOMAN SIYAQ NUMBER ONE THOUSAND
        900: "\U0001ed1b",  # 𞴛 OTTOMAN SIYAQ NUMBER NINE HUNDRED
        800: "\U0001ed1a",  # 𞴚 OTTOMAN SIYAQ NUMBER EIGHT HUNDRED
        700: "\U0001ed19",  # 𞴙 OTTOMAN SIYAQ NUMBER SEVEN HUNDRED
        600: "\U0001ed18",  # 𞴘 OTTOMAN SIYAQ NUMBER SIX HUNDRED
        500: "\U0001ed17",  # 𞴗 OTTOMAN SIYAQ NUMBER FIVE HUNDRED
        400: "\U0001ed16",  # 𞴖 OTTOMAN SIYAQ NUMBER FOUR HUNDRED
        300: "\U0001ed15",  # 𞴕 OTTOMAN SIYAQ NUMBER THREE HUNDRED
        200: "\U0001ed14",  # 𞴔 OTTOMAN SIYAQ NUMBER TWO HUNDRED
        100: "\U0001ed13",  # 𞴓 OTTOMAN SIYAQ NUMBER ONE HUNDRED
        90: "\U0001ed12",  # 𞴒 OTTOMAN SIYAQ NUMBER NINETY
        80: "\U0001ed11",  # 𞴑 OTTOMAN SIYAQ NUMBER EIGHTY
        70: "\U0001ed10",  # 𞴐 OTTOMAN SIYAQ NUMBER SEVENTY
        60: "\U0001ed0f",  # 𞴏 OTTOMAN SIYAQ NUMBER SIXTY
        50: "\U0001ed0e",  # 𞴎 OTTOMAN SIYAQ NUMBER FIFTY
        40: "\U0001ed0d",  # 𞴍 OTTOMAN SIYAQ NUMBER FORTY
        30: "\U0001ed0c",  # 𞴌 OTTOMAN SIYAQ NUMBER THIRTY
        20: "\U0001ed0b",  # 𞴋 OTTOMAN SIYAQ NUMBER TWENTY
        10: "\U0001ed0a",  # 𞴊 OTTOMAN SIYAQ NUMBER TEN
        9: "\U0001ed09",  # 𞴉 OTTOMAN SIYAQ NUMBER NINE
        8: "\U0001ed08",  # 𞴈 OTTOMAN SIYAQ NUMBER EIGHT
        7: "\U0001ed07",  # 𞴇 OTTOMAN SIYAQ NUMBER SEVEN
        6: "\U0001ed06",  # 𞴆 OTTOMAN SIYAQ NUMBER SIX
        5: "\U0001ed05",  # 𞴅 OTTOMAN SIYAQ NUMBER FIVE
        4: "\U0001ed04",  # 𞴄 OTTOMAN SIYAQ NUMBER FOUR
        3: "\U0001ed03",  # 𞴃 OTTOMAN SIYAQ NUMBER THREE
        2: "\U0001ed02",  # 𞴂 OTTOMAN SIYAQ NUMBER TWO
        1: "\U0001ed01",  # 𞴁 OTTOMAN SIYAQ NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {
        **{v: k for k, v in _to_numeral_map.items()},
        "\U0001ed2f": 2,  # 𞴯 OTTOMAN SIYAQ ALTERNATE NUMBER TWO
        "\U0001ed30": 3,  # 𞴰 OTTOMAN SIYAQ ALTERNATE NUMBER THREE
        "\U0001ed31": 4,  # 𞴱 OTTOMAN SIYAQ ALTERNATE NUMBER FOUR
        "\U0001ed32": 5,  # 𞴲 OTTOMAN SIYAQ ALTERNATE NUMBER FIVE
        "\U0001ed33": 6,  # 𞴳 OTTOMAN SIYAQ ALTERNATE NUMBER SIX
        "\U0001ed34": 7,  # 𞴴 OTTOMAN SIYAQ ALTERNATE NUMBER SEVEN
        "\U0001ed35": 8,  # 𞴵 OTTOMAN SIYAQ ALTERNATE NUMBER EIGHT
        "\U0001ed36": 9,  # 𞴶 OTTOMAN SIYAQ ALTERNATE NUMBER NINE
        "\U0001ed37": 10,  # 𞴷 OTTOMAN SIYAQ ALTERNATE NUMBER TEN
        "\U0001ed38": 400,  # 𞴸 OTTOMAN SIYAQ ALTERNATE NUMBER FOUR HUNDRED
        "\U0001ed39": 600,  # 𞴹 OTTOMAN SIYAQ ALTERNATE NUMBER SIX HUNDRED
        "\U0001ed3a": 2000,  # 𞴺 OTTOMAN SIYAQ ALTERNATE NUMBER TWO THOUSAND
        "\U0001ed3b": 10000,  # 𞴻 OTTOMAN SIYAQ ALTERNATE NUMBER TEN THOUSAND
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Ottoman Siyaq numeral representation.

        Selects the unique glyph for each denomination, largest first, then
        reverses so the highest denomination appears rightmost (RTL).

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> OttomanSiyaq._to_numeral(1)
            '𞴁'
            >>> OttomanSiyaq._to_numeral(10)
            '𞴊'
            >>> OttomanSiyaq._to_numeral(100)
            '𞴓'
            >>> OttomanSiyaq._to_numeral(1000)
            '𞴜'
            >>> OttomanSiyaq._to_numeral(10000)
            '𞴥'
            >>> OttomanSiyaq._to_numeral(99999)
            '𞴉𞴒𞴛𞴤𞴭'
        """
        return reversed_greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Ottoman Siyaq numeral string to its Arabic integer value.

        Reverses the input (right-to-left -> left-to-right) then sums the
        values of each glyph. Both standard and alternate glyph forms are
        accepted.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> OttomanSiyaq._from_numeral('𞴁')
            1
            >>> OttomanSiyaq._from_numeral('𞴊')
            10
            >>> OttomanSiyaq._from_numeral('𞴓')
            100
            >>> OttomanSiyaq._from_numeral('𞴜')
            1000
            >>> OttomanSiyaq._from_numeral('𞴥')
            10000
            >>> OttomanSiyaq._from_numeral('𞴉𞴒𞴛𞴤𞴭')
            99999
            >>> OttomanSiyaq._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid OttomanSiyaq character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


class IndicSiyaq(System[str, int]):
    """Implements bidirectional conversion between integers and Indic Siyaq numerals.

    - Uses Unicode block U+1EC70-U+1ECBF (forty-five standard glyphs: units 1-9, decades
      10-90, hundreds 100-900, thousands 1,000-9,000, ten-thousands 10,000-90,000;
      alternate and prefixed forms also accepted as input but not emitted)
    - The system is purely additive with one unique glyph per denomination; written
      right-to-left (largest denomination on the right)
    - Encoding reverses the greedy result; decoding reverses the input before summing

    Attributes:
        minimum: Minimum valid value (1)
        maximum: Maximum valid value (99,999)
        maximum_is_many: False - integers greater than 99,999 are not representable
        encodings: UTF-8 only
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99999
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        90000: "\U0001ec9d",  # 𞲝 INDIC SIYAQ NUMBER NINETY THOUSAND
        80000: "\U0001ec9c",  # 𞲜 INDIC SIYAQ NUMBER EIGHTY THOUSAND
        70000: "\U0001ec9b",  # 𞲛 INDIC SIYAQ NUMBER SEVENTY THOUSAND
        60000: "\U0001ec9a",  # 𞲚 INDIC SIYAQ NUMBER SIXTY THOUSAND
        50000: "\U0001ec99",  # 𞲙 INDIC SIYAQ NUMBER FIFTY THOUSAND
        40000: "\U0001ec98",  # 𞲘 INDIC SIYAQ NUMBER FORTY THOUSAND
        30000: "\U0001ec97",  # 𞲗 INDIC SIYAQ NUMBER THIRTY THOUSAND
        20000: "\U0001ec96",  # 𞲖 INDIC SIYAQ NUMBER TWENTY THOUSAND
        10000: "\U0001ec95",  # 𞲕 INDIC SIYAQ NUMBER TEN THOUSAND
        9000: "\U0001ec94",  # 𞲔 INDIC SIYAQ NUMBER NINE THOUSAND
        8000: "\U0001ec93",  # 𞲓 INDIC SIYAQ NUMBER EIGHT THOUSAND
        7000: "\U0001ec92",  # 𞲒 INDIC SIYAQ NUMBER SEVEN THOUSAND
        6000: "\U0001ec91",  # 𞲑 INDIC SIYAQ NUMBER SIX THOUSAND
        5000: "\U0001ec90",  # 𞲐 INDIC SIYAQ NUMBER FIVE THOUSAND
        4000: "\U0001ec8f",  # 𞲏 INDIC SIYAQ NUMBER FOUR THOUSAND
        3000: "\U0001ec8e",  # 𞲎 INDIC SIYAQ NUMBER THREE THOUSAND
        2000: "\U0001ec8d",  # 𞲍 INDIC SIYAQ NUMBER TWO THOUSAND
        1000: "\U0001ec8c",  # 𞲌 INDIC SIYAQ NUMBER ONE THOUSAND
        900: "\U0001ec8b",  # 𞲋 INDIC SIYAQ NUMBER NINE HUNDRED
        800: "\U0001ec8a",  # 𞲊 INDIC SIYAQ NUMBER EIGHT HUNDRED
        700: "\U0001ec89",  # 𞲉 INDIC SIYAQ NUMBER SEVEN HUNDRED
        600: "\U0001ec88",  # 𞲈 INDIC SIYAQ NUMBER SIX HUNDRED
        500: "\U0001ec87",  # 𞲇 INDIC SIYAQ NUMBER FIVE HUNDRED
        400: "\U0001ec86",  # 𞲆 INDIC SIYAQ NUMBER FOUR HUNDRED
        300: "\U0001ec85",  # 𞲅 INDIC SIYAQ NUMBER THREE HUNDRED
        200: "\U0001ec84",  # 𞲄 INDIC SIYAQ NUMBER TWO HUNDRED
        100: "\U0001ec83",  # 𞲃 INDIC SIYAQ NUMBER ONE HUNDRED
        90: "\U0001ec82",  # 𞲂 INDIC SIYAQ NUMBER NINETY
        80: "\U0001ec81",  # 𞲁 INDIC SIYAQ NUMBER EIGHTY
        70: "\U0001ec80",  # 𞲀 INDIC SIYAQ NUMBER SEVENTY
        60: "\U0001ec7f",  # 𞱿 INDIC SIYAQ NUMBER SIXTY
        50: "\U0001ec7e",  # 𞱾 INDIC SIYAQ NUMBER FIFTY
        40: "\U0001ec7d",  # 𞱽 INDIC SIYAQ NUMBER FORTY
        30: "\U0001ec7c",  # 𞱼 INDIC SIYAQ NUMBER THIRTY
        20: "\U0001ec7b",  # 𞱻 INDIC SIYAQ NUMBER TWENTY
        10: "\U0001ec7a",  # 𞱺 INDIC SIYAQ NUMBER TEN
        9: "\U0001ec79",  # 𞱹 INDIC SIYAQ NUMBER NINE
        8: "\U0001ec78",  # 𞱸 INDIC SIYAQ NUMBER EIGHT
        7: "\U0001ec77",  # 𞱷 INDIC SIYAQ NUMBER SEVEN
        6: "\U0001ec76",  # 𞱶 INDIC SIYAQ NUMBER SIX
        5: "\U0001ec75",  # 𞱵 INDIC SIYAQ NUMBER FIVE
        4: "\U0001ec74",  # 𞱴 INDIC SIYAQ NUMBER FOUR
        3: "\U0001ec73",  # 𞱳 INDIC SIYAQ NUMBER THREE
        2: "\U0001ec72",  # 𞱲 INDIC SIYAQ NUMBER TWO
        1: "\U0001ec71",  # 𞱱 INDIC SIYAQ NUMBER ONE
    }

    _from_numeral_map: Mapping[str, int] = {
        **{v: k for k, v in _to_numeral_map.items()},
        "\U0001eca3": 1,  # 𞲣 INDIC SIYAQ NUMBER PREFIXED ONE
        "\U0001eca4": 2,  # 𞲤 INDIC SIYAQ NUMBER PREFIXED TWO
        "\U0001eca5": 3,  # 𞲥 INDIC SIYAQ NUMBER PREFIXED THREE
        "\U0001eca6": 4,  # 𞲦 INDIC SIYAQ NUMBER PREFIXED FOUR
        "\U0001eca7": 5,  # 𞲧 INDIC SIYAQ NUMBER PREFIXED FIVE
        "\U0001eca8": 6,  # 𞲨 INDIC SIYAQ NUMBER PREFIXED SIX
        "\U0001eca9": 7,  # 𞲩 INDIC SIYAQ NUMBER PREFIXED SEVEN
        "\U0001ecaa": 8,  # 𞲪 INDIC SIYAQ NUMBER PREFIXED EIGHT
        "\U0001ecab": 9,  # 𞲫 INDIC SIYAQ NUMBER PREFIXED NINE
        "\U0001ecb1": 1,  # 𞲱 INDIC SIYAQ NUMBER ALTERNATE ONE
        "\U0001ecb2": 2,  # 𞲲 INDIC SIYAQ NUMBER ALTERNATE TWO
        "\U0001ecb3": 10000,  # 𞲳 INDIC SIYAQ NUMBER ALTERNATE TEN THOUSAND
    }

    @classmethod
    def _to_numeral(cls, denotation: int) -> str:
        """Convert an Arabic integer to its Indic Siyaq numeral representation.

        Selects the unique glyph for each denomination, largest first, then
        reverses so the highest denomination appears rightmost (RTL).

        Args:
            denotation: The Arabic denotation to convert.

        Returns:
            The representation of the denotation in this numeral system.

        Raises:
            ValueError: If the denotation is outside the valid range.

        Examples:
            >>> IndicSiyaq._to_numeral(1)
            '𞱱'
            >>> IndicSiyaq._to_numeral(10)
            '𞱺'
            >>> IndicSiyaq._to_numeral(100)
            '𞲃'
            >>> IndicSiyaq._to_numeral(1000)
            '𞲌'
            >>> IndicSiyaq._to_numeral(10000)
            '𞲕'
            >>> IndicSiyaq._to_numeral(99999)
            '𞱹𞲂𞲋𞲔𞲝'
        """
        return reversed_greedy_additive_to_numeral(denotation, cls._to_numeral_items)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Indic Siyaq numeral string to its Arabic integer value.

        Reverses the input (right-to-left -> left-to-right) then sums the
        values of each glyph. Alternate, prefixed, and standard glyph forms
        are all accepted.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> IndicSiyaq._from_numeral('𞱱')
            1
            >>> IndicSiyaq._from_numeral('𞱺')
            10
            >>> IndicSiyaq._from_numeral('𞲃')
            100
            >>> IndicSiyaq._from_numeral('𞲌')
            1000
            >>> IndicSiyaq._from_numeral('𞲕')
            10000
            >>> IndicSiyaq._from_numeral('𞱹𞲂𞲋𞲔𞲝')
            99999
            >>> IndicSiyaq._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid IndicSiyaq character: '?'
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )
