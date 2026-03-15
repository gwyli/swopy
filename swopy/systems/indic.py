"""Indic numeral system conversion modules.

This module provides conversion utilities for numeral systems originating
from the Indian subcontinent.
"""

# Ignore ambiguous unicode character strings in Indic numerals
# ruff: noqa: RUF002

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
)


class Kharosthi(System[str, int]):
    """Kharosthi numeral system converter.

    Implements bidirectional conversion between integers and Kharosthi numeral
    strings. Kharosthi is a multiplicative-additive system: unit symbols (1–4)
    preceding a hundreds or thousands symbol act as a multiplier for that
    symbol. Tens and units are written additively. The most significant group
    appears first (leftmost) in the stored string.

    Eight distinct Unicode symbols are used:

        𐩀  U+10A40  KHAROSHTHI DIGIT ONE          ->  1
        𐩁  U+10A41  KHAROSHTHI DIGIT TWO          ->  2
        𐩂  U+10A42  KHAROSHTHI DIGIT THREE        ->  3
        𐩃  U+10A43  KHAROSHTHI DIGIT FOUR         ->  4
        𐩄  U+10A44  KHAROSHTHI NUMBER TEN         ->  10
        𐩅  U+10A45  KHAROSHTHI NUMBER TWENTY      ->  20
        𐩆  U+10A46  KHAROSHTHI NUMBER ONE HUNDRED ->  100
        𐩇  U+10A47  KHAROSHTHI NUMBER ONE THOUSAND->  1000

    The structure of a numeral is (each group optional):

        [units_multiplier] 𐩇   — thousands (multiplier omitted when 1)
        [units_multiplier] 𐩆   — hundreds  (multiplier omitted when 1)
        𐩅* 𐩄?                  — tens (additive 20s then optional 10)
        units*                 — ones (additive 4, 3, 2, 1)

    Examples:
        900  ->  𐩃𐩃𐩀𐩆  (nine × 100, where nine = 4+4+1)
        1996 ->  𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁

    Attributes:
        _to_numeral_map: Mapping of the eight base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Kharosthi glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00010a47",  # 𐩇
        100: "\U00010a46",  # 𐩆
        20: "\U00010a45",  # 𐩅
        10: "\U00010a44",  # 𐩄
        4: "\U00010a43",  # 𐩃
        3: "\U00010a42",  # 𐩂
        2: "\U00010a41",  # 𐩁
        1: "\U00010a40",  # 𐩀
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _units_str(cls, n: int) -> str:
        """Express an integer 1–9 as a string of unit glyphs (4, 3, 2, 1).

        Args:
            n: An integer in the range 1–9.

        Returns:
            The greedy representation of ``n`` using unit glyphs.

        Examples:
            >>> Kharosthi._units_str(1)
            '𐩀'
            >>> Kharosthi._units_str(6)
            '𐩃𐩁'
            >>> Kharosthi._units_str(9)
            '𐩃𐩃𐩀'
        """
        result = ""
        for value in (4, 3, 2, 1):
            result += cls._to_numeral_map[value] * (n // value)
            n %= value
        return result

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Kharosthi numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens are written as
        additive 20s then an optional 10. Ones are written as additive unit
        symbols using greedy decomposition with 4, 3, 2, 1.

        Args:
            number: The Arabic number to convert.

        Returns:
            The Kharosthi string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Kharosthi._to_numeral(1)
            '𐩀'
            >>> Kharosthi._to_numeral(9)
            '𐩃𐩃𐩀'
            >>> Kharosthi._to_numeral(10)
            '𐩄'
            >>> Kharosthi._to_numeral(100)
            '𐩆'
            >>> Kharosthi._to_numeral(200)
            '𐩁𐩆'
            >>> Kharosthi._to_numeral(900)
            '𐩃𐩃𐩀𐩆'
            >>> Kharosthi._to_numeral(1000)
            '𐩇'
            >>> Kharosthi._to_numeral(1996)
            '𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁'
            >>> Kharosthi._to_numeral(9999)
            '𐩃𐩃𐩀𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩃𐩀'
        """
        result = ""

        # Thousands group: unit multiplier (omitted if 1) + 𐩇
        thousands, number = divmod(number, 1000)
        if thousands:
            if thousands > 1:
                result += cls._units_str(thousands)
            result += cls._to_numeral_map[1000]

        # Hundreds group: unit multiplier (omitted if 1) + 𐩆
        hundreds, number = divmod(number, 100)
        if hundreds:
            if hundreds > 1:
                result += cls._units_str(hundreds)
            result += cls._to_numeral_map[100]

        # Tens: additive 20s then optional 10
        twenties, number = divmod(number, 20)
        result += cls._to_numeral_map[20] * twenties
        tens, number = divmod(number, 10)
        result += cls._to_numeral_map[10] * tens

        # Ones: additive 4, 3, 2, 1
        result += cls._units_str(number)

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Kharosthi numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𐩀–𐩃) accumulate in a buffer.
        When a hundreds (𐩆) or thousands (𐩇) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty); 20 (𐩅) and 10
        (𐩄) symbols are added directly and flush the unit buffer as additive
        ones first. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Kharosthi numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Kharosthi._from_numeral('𐩃𐩃𐩀')
            9
            >>> Kharosthi._from_numeral('𐩃𐩃𐩀𐩆')
            900
            >>> Kharosthi._from_numeral('𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁')
            1996
        """
        unit_chars = frozenset(cls._to_numeral_map[v] for v in (1, 2, 3, 4))
        multiplier_chars = {
            cls._to_numeral_map[100]: 100,
            cls._to_numeral_map[1000]: 1000,
        }
        additive_chars = {
            cls._to_numeral_map[10]: 10,
            cls._to_numeral_map[20]: 20,
        }
        valid_chars = set(cls._from_numeral_map.keys())

        total = 0
        unit_buffer = 0

        for char in numeral:
            if char not in valid_chars:
                raise ValueError(f"Invalid Kharosthi character: {char!r}")

            if char in unit_chars:
                unit_buffer += cls._from_numeral_map[char]
            elif char in multiplier_chars:
                total += multiplier_chars[char] * max(unit_buffer, 1)
                unit_buffer = 0
            else:
                # Additive tens symbol: flush accumulated units as ones first
                total += unit_buffer
                unit_buffer = 0
                total += additive_chars[char]

        total += unit_buffer
        return total


class Brahmi(System[str, int]):
    """Brahmi numeral system converter.

    Implements bidirectional conversion between integers and Brahmi numeral
    strings. Brahmi is a multiplicative-additive system: unit symbols (1–9)
    preceding a hundreds or thousands symbol act as a multiplier for that
    symbol (omitted when 1). Each decade (10–90) has its own distinct symbol;
    ones are written directly. The most significant group appears first
    (leftmost).

    Twenty distinct Unicode symbols are used:

        𑁒  U+11052  BRAHMI NUMBER ONE          ->  1
        𑁓  U+11053  BRAHMI NUMBER TWO          ->  2
        𑁔  U+11054  BRAHMI NUMBER THREE        ->  3
        𑁕  U+11055  BRAHMI NUMBER FOUR         ->  4
        𑁖  U+11056  BRAHMI NUMBER FIVE         ->  5
        𑁗  U+11057  BRAHMI NUMBER SIX          ->  6
        𑁘  U+11058  BRAHMI NUMBER SEVEN        ->  7
        𑁙  U+11059  BRAHMI NUMBER EIGHT        ->  8
        𑁚  U+1105A  BRAHMI NUMBER NINE         ->  9
        𑁛  U+1105B  BRAHMI NUMBER TEN          ->  10
        𑁜  U+1105C  BRAHMI NUMBER TWENTY       ->  20
        𑁝  U+1105D  BRAHMI NUMBER THIRTY       ->  30
        𑁞  U+1105E  BRAHMI NUMBER FORTY        ->  40
        𑁟  U+1105F  BRAHMI NUMBER FIFTY        ->  50
        𑁠  U+11060  BRAHMI NUMBER SIXTY        ->  60
        𑁡  U+11061  BRAHMI NUMBER SEVENTY      ->  70
        𑁢  U+11062  BRAHMI NUMBER EIGHTY       ->  80
        𑁣  U+11063  BRAHMI NUMBER NINETY       ->  90
        𑁤  U+11064  BRAHMI NUMBER ONE HUNDRED  ->  100
        𑁥  U+11065  BRAHMI NUMBER ONE THOUSAND ->  1000

    The structure of a numeral is (each group optional):

        [unit_multiplier] 𑁥  — thousands (multiplier omitted when 1)
        [unit_multiplier] 𑁤  — hundreds  (multiplier omitted when 1)
        decade_symbol?        — one of 𑁛–𑁣 (10, 20, …, 90)
        unit_symbol?          — one of 𑁒–𑁚 (1–9)

    Examples:
        200  ->  𑁓𑁤  (two × 100)
        999  ->  𑁚𑁤𑁣𑁚  (nine × 100, ninety, nine)
        1996 ->  𑁥𑁚𑁤𑁣𑁗

    Attributes:
        _to_numeral_map: Mapping of the twenty base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Brahmi glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U00011065",  # 𑁥
        100: "\U00011064",  # 𑁤
        90: "\U00011063",  # 𑁣
        80: "\U00011062",  # 𑁢
        70: "\U00011061",  # 𑁡
        60: "\U00011060",  # 𑁠
        50: "\U0001105f",  # 𑁟
        40: "\U0001105e",  # 𑁞
        30: "\U0001105d",  # 𑁝
        20: "\U0001105c",  # 𑁜
        10: "\U0001105b",  # 𑁛
        9: "\U0001105a",  # 𑁚
        8: "\U00011059",  # 𑁙
        7: "\U00011058",  # 𑁘
        6: "\U00011057",  # 𑁗
        5: "\U00011056",  # 𑁖
        4: "\U00011055",  # 𑁕
        3: "\U00011054",  # 𑁔
        2: "\U00011053",  # 𑁓
        1: "\U00011052",  # 𑁒
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Brahmi numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10–90). Ones use a dedicated unit symbol (1–9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The Brahmi string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Brahmi._to_numeral(1)
            '𑁒'
            >>> Brahmi._to_numeral(9)
            '𑁚'
            >>> Brahmi._to_numeral(10)
            '𑁛'
            >>> Brahmi._to_numeral(11)
            '𑁛𑁒'
            >>> Brahmi._to_numeral(99)
            '𑁣𑁚'
            >>> Brahmi._to_numeral(100)
            '𑁤'
            >>> Brahmi._to_numeral(200)
            '𑁓𑁤'
            >>> Brahmi._to_numeral(999)
            '𑁚𑁤𑁣𑁚'
            >>> Brahmi._to_numeral(1000)
            '𑁥'
            >>> Brahmi._to_numeral(1996)
            '𑁥𑁚𑁤𑁣𑁗'
            >>> Brahmi._to_numeral(9999)
            '𑁚𑁥𑁚𑁤𑁣𑁚'
        """
        return multiplicative_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Brahmi numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𑁒–𑁚) accumulate in a buffer.
        When a hundreds (𑁤) or thousands (𑁥) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑁛–𑁣) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Brahmi numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Brahmi._from_numeral('𑁚')
            9
            >>> Brahmi._from_numeral('𑁚𑁤𑁣𑁚')
            999
            >>> Brahmi._from_numeral('𑁥𑁚𑁤𑁣𑁗')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, "Brahmi"
        )


class Bakhshali(System[str, int]):
    """Bakhshali (Sinhala Archaic) numeral system converter.

    Implements bidirectional conversion between integers and Bakhshali numeral
    strings. The system is multiplicative-additive, identical in structure to
    Brahmi: unit symbols (1–9) preceding a hundreds or thousands symbol act as
    a multiplier (omitted when 1); each decade (10–90) has its own symbol;
    ones are written directly. The most significant group appears first.

    Twenty distinct Unicode symbols are used:

        𑇡  U+111E1  SINHALA ARCHAIC DIGIT ONE          ->  1
        𑇢  U+111E2  SINHALA ARCHAIC DIGIT TWO          ->  2
        𑇣  U+111E3  SINHALA ARCHAIC DIGIT THREE        ->  3
        𑇤  U+111E4  SINHALA ARCHAIC DIGIT FOUR         ->  4
        𑇥  U+111E5  SINHALA ARCHAIC DIGIT FIVE         ->  5
        𑇦  U+111E6  SINHALA ARCHAIC DIGIT SIX          ->  6
        𑇧  U+111E7  SINHALA ARCHAIC DIGIT SEVEN        ->  7
        𑇨  U+111E8  SINHALA ARCHAIC DIGIT EIGHT        ->  8
        𑇩  U+111E9  SINHALA ARCHAIC DIGIT NINE         ->  9
        𑇪  U+111EA  SINHALA ARCHAIC NUMBER TEN         ->  10
        𑇫  U+111EB  SINHALA ARCHAIC NUMBER TWENTY      ->  20
        𑇬  U+111EC  SINHALA ARCHAIC NUMBER THIRTY      ->  30
        𑇭  U+111ED  SINHALA ARCHAIC NUMBER FORTY       ->  40
        𑇮  U+111EE  SINHALA ARCHAIC NUMBER FIFTY       ->  50
        𑇯  U+111EF  SINHALA ARCHAIC NUMBER SIXTY       ->  60
        𑇰  U+111F0  SINHALA ARCHAIC NUMBER SEVENTY     ->  70
        𑇱  U+111F1  SINHALA ARCHAIC NUMBER EIGHTY      ->  80
        𑇲  U+111F2  SINHALA ARCHAIC NUMBER NINETY      ->  90
        𑇳  U+111F3  SINHALA ARCHAIC NUMBER ONE HUNDRED ->  100
        𑇴  U+111F4  SINHALA ARCHAIC NUMBER ONE THOUSAND->  1000

    The structure of a numeral is (each group optional):

        [unit_multiplier] 𑇴  — thousands (multiplier omitted when 1)
        [unit_multiplier] 𑇳  — hundreds  (multiplier omitted when 1)
        decade_symbol?        — one of 𑇪–𑇲 (10, 20, …, 90)
        unit_symbol?          — one of 𑇡–𑇩 (1–9)

    Examples:
        200  ->  𑇢𑇳  (two × 100)
        999  ->  𑇩𑇳𑇲𑇩  (nine × 100, ninety, nine)
        1996 ->  𑇴𑇩𑇳𑇲𑇦

    Attributes:
        _to_numeral_map: Mapping of the twenty base values to their glyphs.
        _from_numeral_map: Mapping of glyphs to their base integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        maximum_is_many: False; 9999 is a precise upper bound.
        encodings: UTF-8 only; Bakhshali glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        1000: "\U000111f4",  # 𑇴
        100: "\U000111f3",  # 𑇳
        90: "\U000111f2",  # 𑇲
        80: "\U000111f1",  # 𑇱
        70: "\U000111f0",  # 𑇰
        60: "\U000111ef",  # 𑇯
        50: "\U000111ee",  # 𑇮
        40: "\U000111ed",  # 𑇭
        30: "\U000111ec",  # 𑇬
        20: "\U000111eb",  # 𑇫
        10: "\U000111ea",  # 𑇪
        9: "\U000111e9",  # 𑇩
        8: "\U000111e8",  # 𑇨
        7: "\U000111e7",  # 𑇧
        6: "\U000111e6",  # 𑇦
        5: "\U000111e5",  # 𑇥
        4: "\U000111e4",  # 𑇤
        3: "\U000111e3",  # 𑇣
        2: "\U000111e2",  # 𑇢
        1: "\U000111e1",  # 𑇡
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Bakhshali numeral representation.

        Thousands and hundreds groups are written as a unit-symbol multiplier
        (omitted when 1) followed by the group symbol. Tens use a dedicated
        decade symbol (10–90). Ones use a dedicated unit symbol (1–9).

        Args:
            number: The Arabic number to convert.

        Returns:
            The Bakhshali string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Bakhshali._to_numeral(1)
            '𑇡'
            >>> Bakhshali._to_numeral(9)
            '𑇩'
            >>> Bakhshali._to_numeral(10)
            '𑇪'
            >>> Bakhshali._to_numeral(11)
            '𑇪𑇡'
            >>> Bakhshali._to_numeral(99)
            '𑇲𑇩'
            >>> Bakhshali._to_numeral(100)
            '𑇳'
            >>> Bakhshali._to_numeral(200)
            '𑇢𑇳'
            >>> Bakhshali._to_numeral(999)
            '𑇩𑇳𑇲𑇩'
            >>> Bakhshali._to_numeral(1000)
            '𑇴'
            >>> Bakhshali._to_numeral(1996)
            '𑇴𑇩𑇳𑇲𑇦'
            >>> Bakhshali._to_numeral(9999)
            '𑇩𑇴𑇩𑇳𑇲𑇩'
        """
        return multiplicative_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Bakhshali numeral string to its Arabic integer value.

        Scans left-to-right. Unit symbols (𑇡–𑇩) accumulate in a buffer.
        When a hundreds (𑇳) or thousands (𑇴) symbol is encountered the buffer
        is treated as a multiplier (defaulting to 1 when empty) and is reset.
        Decade symbols (𑇪–𑇲) flush the unit buffer as additive ones then add
        their face value. Any remaining buffer is added as ones at the end.

        Args:
            numeral: The Bakhshali numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Bakhshali._from_numeral('𑇩')
            9
            >>> Bakhshali._from_numeral('𑇩𑇳𑇲𑇩')
            999
            >>> Bakhshali._from_numeral('𑇴𑇩𑇳𑇲𑇦')
            1996
        """
        return multiplicative_additive_from_numeral(
            numeral, cls._from_numeral_map, "Bakhshali"
        )
