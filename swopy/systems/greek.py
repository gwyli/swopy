"""Greek and Etruscan numeral system converters.

This module implements numeral systems from the Greek and Etruscan script
families.
Currently supports:

    Milesian    U+0370-U+03FF  (Greek alphabetic numerals; U+0375 prefix for
                                thousands)
    Alphabetic  U+0370-U+03FF  (uppercase Greek alphabetic numerals; U+0374
                                keraia suffix as number mark)
    Aegean      U+10107-U+10133  (45 glyphs for 1–90,000)
    Attic       U+0394-U+039C (Greek letters) + U+10140-U+10147 (acrophonic)
    Etruscan    U+10320-U+10323  (four glyphs: 1, 5, 10, 50)

Milesian uses lowercase Greek alphabetic numerals; each letter contributes its
face value and numerals are written largest-to-smallest.  Thousands are
denoted by the Greek numeral sign ͵ (U+0375) before the corresponding unit
letter.

Alphabetic is the uppercase variant of the same Greek alphabetic numeral
system.  The keraia ʹ (U+0374) is appended as a number mark; thousands use
the same ͵ (U+0375) prefix as Milesian.  Both upper- and lower-case letters
are accepted in decoding, and a trailing keraia is optional.

Aegean is a purely additive system using dedicated number glyphs; each
denomination appears at most once, written largest-to-smallest.

Attic is a purely additive system using Greek letter acrophonics for base
denominations and composite symbols for fives; it also supports base-4
fractions (1/4, 1/2, 3/4).

Etruscan is a purely additive right-to-left system; encoding reverses the
greedy result so the highest-denomination glyphs appear on the right, and
decoding reverses the input before summing.
"""

# Ignore ambiguous unicode character strings in Greek and Etruscan numerals
# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import ClassVar

from ..system import Encodings, System
from ._algorithms import (
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    longest_match_from_numeral,
    reversed_char_sum_from_numeral,
    reversed_greedy_additive_to_numeral,
)


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
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

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
        return longest_match_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Aegean(System[str, int]):
    """Aegean numeral system converter.

    Implements bidirectional conversion between integers and Aegean (Linear A/B)
    numeral strings. Aegean is a purely additive, base-10 system: each
    denomination from 1 through 90,000 has its own unique Unicode symbol, and
    numerals are formed by concatenating symbols in descending order. Each symbol
    appears at most once.

    Forty-five distinct Unicode symbols are used (U+10107–U+10133):

        𐄇–𐄏  U+10107–U+1010F  AEGEAN NUMBER ONE through NINE         ->  1–9
        𐄐–𐄘  U+10110–U+10118  AEGEAN NUMBER TEN through NINETY       ->  10–90
        𐄙–𐄡  U+10119–U+10121  AEGEAN NUMBER ONE HUNDRED through      ->  100–900
                                NINE HUNDRED
        𐄢–𐄪  U+10122–U+1012A  AEGEAN NUMBER ONE THOUSAND through     ->  1000–9000
                                NINE THOUSAND
        𐄫–𐄳  U+1012B–U+10133  AEGEAN NUMBER TEN THOUSAND through     ->  10000–90000
                                NINETY THOUSAND

    The structure of a numeral is (each symbol optional, at most one per row):

        [ten-thousand symbol]  — one of 𐄫–𐄳 (10000, 20000, …, 90000)
        [thousand symbol]      — one of 𐄢–𐄪 (1000, 2000, …, 9000)
        [hundred symbol]       — one of 𐄙–𐄡 (100, 200, …, 900)
        [ten symbol]           — one of 𐄐–𐄘 (10, 20, …, 90)
        [unit symbol]          — one of 𐄇–𐄏 (1, 2, …, 9)

    Examples:
        1996  ->  𐄢𐄡𐄘𐄌  (1000 + 900 + 90 + 6)
        99999 ->  𐄳𐄪𐄡𐄘𐄏  (90000 + 9000 + 900 + 90 + 9)

    Attributes:
        _to_numeral_map: Mapping of the 45 denominations to their glyphs.
        _from_numeral_map: Mapping of glyphs to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (99999).
        maximum_is_many: False; 99999 is a precise upper bound.
        encodings: UTF-8 only; Aegean glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 99999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        90000: "\U00010133",  # 𐄳
        80000: "\U00010132",  # 𐄲
        70000: "\U00010131",  # 𐄱
        60000: "\U00010130",  # 𐄰
        50000: "\U0001012f",  # 𐄯
        40000: "\U0001012e",  # 𐄮
        30000: "\U0001012d",  # 𐄭
        20000: "\U0001012c",  # 𐄬
        10000: "\U0001012b",  # 𐄫
        9000: "\U0001012a",  # 𐄪
        8000: "\U00010129",  # 𐄩
        7000: "\U00010128",  # 𐄨
        6000: "\U00010127",  # 𐄧
        5000: "\U00010126",  # 𐄦
        4000: "\U00010125",  # 𐄥
        3000: "\U00010124",  # 𐄤
        2000: "\U00010123",  # 𐄣
        1000: "\U00010122",  # 𐄢
        900: "\U00010121",  # 𐄡
        800: "\U00010120",  # 𐄠
        700: "\U0001011f",  # 𐄟
        600: "\U0001011e",  # 𐄞
        500: "\U0001011d",  # 𐄝
        400: "\U0001011c",  # 𐄜
        300: "\U0001011b",  # 𐄛
        200: "\U0001011a",  # 𐄚
        100: "\U00010119",  # 𐄙
        90: "\U00010118",  # 𐄘
        80: "\U00010117",  # 𐄗
        70: "\U00010116",  # 𐄖
        60: "\U00010115",  # 𐄕
        50: "\U00010114",  # 𐄔
        40: "\U00010113",  # 𐄓
        30: "\U00010112",  # 𐄒
        20: "\U00010111",  # 𐄑
        10: "\U00010110",  # 𐄐
        9: "\U0001010f",  # 𐄏
        8: "\U0001010e",  # 𐄎
        7: "\U0001010d",  # 𐄍
        6: "\U0001010c",  # 𐄌
        5: "\U0001010b",  # 𐄋
        4: "\U0001010a",  # 𐄊
        3: "\U00010109",  # 𐄉
        2: "\U00010108",  # 𐄈
        1: "\U00010107",  # 𐄇
    }

    _from_numeral_map: Mapping[str, int] = {v: k for k, v in _to_numeral_map.items()}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Aegean numeral representation.

        Uses greedy decomposition: at each step the largest denomination not
        exceeding the remainder is consumed, producing numerals in
        largest-to-smallest order. Each symbol appears at most once.

        Args:
            number: The Arabic number to convert.

        Returns:
            The Aegean string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range.

        Examples:
            >>> Aegean._to_numeral(1)
            '𐄇'
            >>> Aegean._to_numeral(9)
            '𐄏'
            >>> Aegean._to_numeral(10)
            '𐄐'
            >>> Aegean._to_numeral(99)
            '𐄘𐄏'
            >>> Aegean._to_numeral(1000)
            '𐄢'
            >>> Aegean._to_numeral(1996)
            '𐄢𐄡𐄘𐄌'
            >>> Aegean._to_numeral(99999)
            '𐄳𐄪𐄡𐄘𐄏'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Aegean numeral string to its Arabic integer value.

        Scans left-to-right, looking each character up in the value map and
        summing the results.

        Args:
            numeral: The Aegean numeral string to convert.

        Returns:
            The integer value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Aegean._from_numeral('𐄇')
            1
            >>> Aegean._from_numeral('𐄢𐄡𐄘𐄌')
            1996
            >>> Aegean._from_numeral('𐄳𐄪𐄡𐄘𐄏')
            99999
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Attic(System[str, int | Fraction]):
    """Greek Attic (acrophonic) numeral system converter.

    Implements bidirectional conversion between integers or fractions and Greek
    Attic numeral strings. Attic is a purely additive system written
    largest-to-smallest. Five composite acrophonic symbols represent 5, 50, 500,
    5000, and 50,000; the base denominations 1, 10, 100, 1000, and 10,000 are
    represented by the Greek letters Ι, Δ, Η, Χ, and Μ respectively. Two
    fraction symbols represent 1/2 and 1/4; the maximum representable fraction
    component is 3/4 (= 𐅁𐅀).

    Twelve distinct symbols are used:

        𐅀  U+10140  GREEK ACROPHONIC ATTIC ONE QUARTER  ->  1/4
        𐅁  U+10141  GREEK ACROPHONIC ATTIC ONE HALF     ->  1/2
        Ι   U+0399   GREEK CAPITAL LETTER IOTA           ->  1
        𐅃  U+10143  GREEK ACROPHONIC ATTIC FIVE         ->  5
        Δ   U+0394   GREEK CAPITAL LETTER DELTA          ->  10
        𐅄  U+10144  GREEK ACROPHONIC ATTIC FIFTY        ->  50
        Η   U+0397   GREEK CAPITAL LETTER ETA            ->  100
        𐅅  U+10145  GREEK ACROPHONIC ATTIC FIVE HUNDRED ->  500
        Χ   U+03A7   GREEK CAPITAL LETTER CHI            ->  1000
        𐅆  U+10146  GREEK ACROPHONIC ATTIC FIVE THOUSAND->  5000
        Μ   U+039C   GREEK CAPITAL LETTER MU             ->  10000
        𐅇  U+10147  GREEK ACROPHONIC ATTIC FIFTY THOUSAND->  50000

    The structure of a numeral is (each group optional):

        𐅇? Μ{0–4}  — fifty-thousands then ten-thousands
        𐅆? Χ{0–4}  — five-thousands then thousands
        𐅅? Η{0–4}  — five-hundreds then hundreds
        𐅄? Δ{0–4}  — fifties then tens
        𐅃? Ι{0–4}  — fives then ones
        𐅁? 𐅀?      — one-half then one-quarter (fractional part only)

    Examples:
        1996  ->  Χ𐅅ΗΗΗΗ𐅄ΔΔΔΔ𐅃Ι
        99999 ->  𐅇ΜΜΜΜ𐅆ΧΧΧΧ𐅅ΗΗΗΗ𐅄ΔΔΔΔ𐅃ΙΙΙΙ

    Attributes:
        _to_numeral_map: Mapping of the twelve base values (int and Fraction) to
            their glyphs, ordered largest-to-smallest.
        _from_numeral_map: Mapping of glyphs (both upper- and lowercase for the
            Greek letters) to their integer or Fraction values.
        minimum: Minimum valid value (1/4).
        maximum: Maximum valid value (99999).
        maximum_is_many: False; 99999 is a precise upper bound.
        encodings: UTF-8 only; Attic acrophonic glyphs have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = Fraction(1, 4)
    maximum: ClassVar[int | float | Fraction] = 99999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int | Fraction, str] = {
        50000: "\U00010147",  # 𐅇
        10000: "\u039c",  # Μ
        5000: "\U00010146",  # 𐅆
        1000: "\u03a7",  # Χ
        500: "\U00010145",  # 𐅅
        100: "\u0397",  # Η
        50: "\U00010144",  # 𐅄
        10: "\u0394",  # Δ
        5: "\U00010143",  # 𐅃
        1: "\u0399",  # Ι
        Fraction(1, 2): "\U00010141",  # 𐅁
        Fraction(1, 4): "\U00010140",  # 𐅀
    }

    # Both uppercase and lowercase Greek letters are included so that either
    # form is accepted as input.
    _from_numeral_map: Mapping[str, int | Fraction] = {
        "\U00010140": Fraction(1, 4),  # 𐅀
        "\U00010141": Fraction(1, 2),  # 𐅁
        "\U00010143": 5,  # 𐅃
        "\U00010144": 50,  # 𐅄
        "\U00010145": 500,  # 𐅅
        "\U00010146": 5000,  # 𐅆
        "\U00010147": 50000,  # 𐅇
        "\u0399": 1,  # Ι  (iota uppercase)
        "\u03b9": 1,  # ι  (iota lowercase)
        "\u0394": 10,  # Δ  (delta uppercase)
        "\u03b4": 10,  # δ  (delta lowercase)
        "\u0397": 100,  # Η  (eta uppercase)
        "\u03b7": 100,  # η  (eta lowercase)
        "\u03a7": 1000,  # Χ  (chi uppercase)
        "\u03c7": 1000,  # χ  (chi lowercase)
        "\u039c": 10000,  # Μ  (mu uppercase)
        "\u03bc": 10000,  # μ  (mu lowercase)
    }

    @classmethod
    def _to_numeral(cls, number: int | Fraction) -> str:
        """Convert an Arabic integer or Fraction to its Attic numeral representation.

        Separates the integer and fractional parts. The integer part is
        decomposed greedily from largest denomination to smallest. The fractional
        part (if any) is expressed using the half (𐅁) and/or quarter (𐅀) symbols
        appended after the integer symbols. Only fractions whose component is
        exactly 0, 1/4, 1/2, or 3/4 are representable.

        Args:
            number: The Arabic number to convert.

        Returns:
            The Attic string representation of ``number``.

        Raises:
            ValueError: If ``number`` is outside the valid range or its
                fractional part is not a multiple of 1/4.

        Examples:
            >>> Attic._to_numeral(1)
            'Ι'
            >>> Attic._to_numeral(5)
            '𐅃'
            >>> Attic._to_numeral(10)
            'Δ'
            >>> from fractions import Fraction
            >>> Attic._to_numeral(Fraction(1, 4))
            '𐅀'
            >>> Attic._to_numeral(Fraction(3, 4))
            '𐅁𐅀'
            >>> Attic._to_numeral(1996)
            'Χ𐅅ΗΗΗΗ𐅄ΔΔΔΔ𐅃Ι'
            >>> Attic._to_numeral(99999)
            '𐅇ΜΜΜΜ𐅆ΧΧΧΧ𐅅ΗΗΗΗ𐅄ΔΔΔΔ𐅃ΙΙΙΙ'
        """
        n = Fraction(number)
        integer_part = int(n)
        frac_part = n - integer_part

        result = ""
        for value, glyph in cls._to_numeral_map.items():
            if isinstance(value, Fraction):
                continue
            count, integer_part = divmod(integer_part, value)
            result += glyph * count

        if frac_part >= Fraction(1, 2):
            result += cls._to_numeral_map[Fraction(1, 2)]
            frac_part -= Fraction(1, 2)
        if frac_part >= Fraction(1, 4):
            result += cls._to_numeral_map[Fraction(1, 4)]
            frac_part -= Fraction(1, 4)
        if frac_part:
            raise ValueError(f"{number} cannot be represented in {cls.__name__}.")

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int | Fraction:
        """Convert an Attic numeral string to its Arabic integer or Fraction value.

        Scans left-to-right, looking each character up in the value map and
        summing the results. Both uppercase and lowercase Greek letters are
        accepted. Returns an ``int`` when the result is a whole number and a
        ``Fraction`` when the result has a fractional component.

        Args:
            numeral: The Attic numeral string to convert.

        Returns:
            The integer or Fraction value of ``numeral``.

        Raises:
            ValueError: If ``numeral`` contains an unrecognised character.

        Examples:
            >>> Attic._from_numeral('Ι')
            1
            >>> Attic._from_numeral('𐅃Ι')
            6
            >>> Attic._from_numeral('Χ𐅅ΗΗΗΗ𐅄ΔΔΔΔ𐅃Ι')
            1996
            >>> from fractions import Fraction
            >>> Attic._from_numeral('𐅁𐅀')
            Fraction(3, 4)
        """
        return char_sum_from_numeral(numeral, cls._from_numeral_map, cls.__name__)


class Etruscan(System[str, int]):
    """Etruscan numeral system converter.

    Implements bidirectional conversion between integers and Etruscan numeral strings.

    Etruscan numerals are a purely additive system written right-to-left (largest
    denomination on the right).  ``_to_numeral`` builds numerals using a greedy
    decomposition (largest denomination first) and reverses the result so that
    the highest-denomination glyphs appear on the right.  ``_from_numeral``
    reverses the input string before summing, so both paths share the same
    left-to-right internal iteration.

    Attributes:
        to_numeral_map: Mapping of integer values to Etruscan numeral components,
            ordered by magnitude including subtractive pairs.
        from_numeral_map: Mapping of Etruscan numeral characters to their integer
            values.
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (399), limited by Etruscan numeral notation.
        maximum_is_many: False, as 399 is a precise limit.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 399

    _to_numeral_map: Mapping[int, str] = {
        50: "\U00010323",  # 𐌣 - OLD ITALIC NUMERAL FIFTY
        10: "\U00010322",  # 𐌢 - OLD ITALIC NUMERAL TEN
        5: "\U00010321",  # 𐌡 - OLD ITALIC NUMERAL FIVE
        1: "\U00010320",  # 𐌠 - OLD ITALIC NUMERAL ONE
    }

    _from_numeral_map: Mapping[str, int] = {
        "\U00010320": 1,
        "\U00010321": 5,
        "\U00010322": 10,
        "\U00010323": 50,
        "I": 1,
        "Λ": 5,
        "X": 10,
        "↑": 50,
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Etruscan numeral representation.

        Uses a greedy decomposition (largest denomination first), then reverses
        the result so the highest-denomination glyphs appear on the right, in
        keeping with the Etruscan right-to-left writing convention.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Etruscan._to_numeral(1)
            '𐌠'
            >>> Etruscan._to_numeral(4)
            '𐌠𐌠𐌠𐌠'
            >>> Etruscan._to_numeral(6)
            '𐌠𐌡'
            >>> Etruscan._to_numeral(10)
            '𐌢'
            >>> Etruscan._to_numeral(17)
            '𐌠𐌠𐌡𐌢'
            >>> Etruscan._to_numeral(29)
            '𐌠𐌠𐌠𐌠𐌡𐌢𐌢'
            >>> Etruscan._to_numeral(55)
            '𐌡𐌣'
            >>> Etruscan._to_numeral(399)
            '𐌠𐌠𐌠𐌠𐌡𐌢𐌢𐌢𐌢𐌣𐌣𐌣𐌣𐌣𐌣𐌣'
        """
        return reversed_greedy_additive_to_numeral(number, cls._to_numeral_map)

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert an Etruscan numeral string to its Arabic integer value.

        Accepts both Unicode glyphs (e.g. ``'𐌠𐌡'``) and their ASCII equivalents
        (e.g. ``'IΛ'``).  The string is expected in standard right-to-left reading
        order (largest denomination on the right), so it is reversed internally
        before summing.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Etruscan._from_numeral('𐌠𐌠𐌠𐌠')
            4
            >>> Etruscan._from_numeral('𐌠𐌡')
            6
            >>> Etruscan._from_numeral('𐌠𐌠𐌡𐌢')
            17
            >>> Etruscan._from_numeral('𐌠𐌠𐌠𐌠𐌡𐌢𐌢')
            29
            >>> Etruscan._from_numeral('IIΛX')
            17
            >>> Etruscan._from_numeral('IIIIΛXX')
            29
        """
        return reversed_char_sum_from_numeral(
            numeral, cls._from_numeral_map, cls.__name__
        )


_KERAIA = "\u0374"  # ʹ  GREEK NUMERAL SIGN (keraia suffix)


class Alphabetic(System[str, int]):
    """Greek Alphabetic numeral system converter.

    Implements bidirectional conversion between integers and Greek alphabetic
    numeral strings.  The system is the uppercase variant of the Milesian
    system: each uppercase letter contributes its face value and numerals are
    written largest-to-smallest.  Thousands are denoted by the Greek numeral
    sign ͵ (U+0375) placed before the corresponding unit letter.  The keraia
    ʹ (U+0374) is appended as a number mark in encoding and stripped (if
    present) before decoding.

    Both upper- and lower-case letters are accepted in ``from_numeral``.

    Attributes:
        minimum: Minimum valid value (1).
        maximum: Maximum valid value (9999).
        encodings: UTF-8 only; Greek letters have no ASCII equivalents.
    """

    minimum: ClassVar[int | float | Fraction] = 1
    maximum: ClassVar[int | float | Fraction] = 9999

    encodings: ClassVar[Encodings] = {"utf8"}

    _to_numeral_map: Mapping[int, str] = {
        9000: "\u0375\u0398",  # ͵Θ
        8000: "\u0375\u0397",  # ͵Η
        7000: "\u0375\u0396",  # ͵Ζ
        6000: "\u0375\u03da",  # ͵Ϛ
        5000: "\u0375\u0395",  # ͵Ε
        4000: "\u0375\u0394",  # ͵Δ
        3000: "\u0375\u0393",  # ͵Γ
        2000: "\u0375\u0392",  # ͵Β
        1000: "\u0375\u0391",  # ͵Α
        900: "\u03e0",  # Ϡ  sampi
        800: "\u03a9",  # Ω
        700: "\u03a8",  # Ψ
        600: "\u03a7",  # Χ
        500: "\u03a6",  # Φ
        400: "\u03a5",  # Υ
        300: "\u03a4",  # Τ
        200: "\u03a3",  # Σ
        100: "\u03a1",  # Ρ
        90: "\u03d8",  # Ϙ  koppa
        80: "\u03a0",  # Π
        70: "\u039f",  # Ο
        60: "\u039e",  # Ξ
        50: "\u039d",  # Ν
        40: "\u039c",  # Μ
        30: "\u039b",  # Λ
        20: "\u039a",  # Κ
        10: "\u0399",  # Ι
        9: "\u0398",  # Θ
        8: "\u0397",  # Η
        7: "\u0396",  # Ζ
        6: "\u03da",  # Ϛ  stigma (uppercase)
        5: "\u0395",  # Ε
        4: "\u0394",  # Δ
        3: "\u0393",  # Γ
        2: "\u0392",  # Β
        1: "\u0391",  # Α
    }

    # Two-character thousands tokens come first; both upper- and lower-case
    # single-character tokens are included so either form is accepted.
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
        "\u03d8": 90,  # Ϙ koppa (uppercase)
        "\u03d9": 90,  # ϙ koppa (lowercase)
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
        "\u03e0": 900,  # Ϡ sampi (uppercase)
        "\u03e1": 900,  # ϡ sampi (lowercase)
    }

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Convert an Arabic integer to its Greek Alphabetic numeral.

        Uses greedy additive decomposition with uppercase letters, largest
        denomination first, then appends the keraia ʹ (U+0374) as a number
        mark.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Alphabetic._to_numeral(1)
            'Αʹ'
            >>> Alphabetic._to_numeral(6)
            'Ϛʹ'
            >>> Alphabetic._to_numeral(9)
            'Θʹ'
            >>> Alphabetic._to_numeral(100)
            'Ρʹ'
            >>> Alphabetic._to_numeral(1000)
            '͵Αʹ'
            >>> Alphabetic._to_numeral(9999)
            '͵ΘϠϘΘʹ'
        """
        return greedy_additive_to_numeral(number, cls._to_numeral_map) + _KERAIA

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Convert a Greek Alphabetic numeral string to its Arabic integer value.

        Strips an optional trailing keraia ʹ (U+0374) before parsing.
        Two-character thousands tokens (͵X) are resolved before their
        constituent single-character entries.  Both upper- and lower-case
        letters are accepted.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside
                the valid range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Alphabetic._from_numeral('Αʹ')
            1
            >>> Alphabetic._from_numeral('α')
            1
            >>> Alphabetic._from_numeral('Θʹ')
            9
            >>> Alphabetic._from_numeral('Ρʹ')
            100
            >>> Alphabetic._from_numeral('͵Αʹ')
            1000
            >>> Alphabetic._from_numeral('͵ΘϠϘΘʹ')
            9999
            >>> Alphabetic._from_numeral('?')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Alphabetic character at position 0: '?'
        """
        if numeral.endswith(_KERAIA):
            numeral = numeral[:-1]
        return longest_match_from_numeral(numeral, cls._from_numeral_map, cls.__name__)
