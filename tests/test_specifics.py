"""
Tests for specific cases

This module is for non-property-based system specific tests. Each system should
have its own class for organisation in the form Test<Module><Class>
"""

# Ignore ambiguous unicode character strings in Roman numerals (e.g., 'I' vs 'Ⅰ').
# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction
from typing import Any, ClassVar

import pytest
from hypothesis import given, strategies

from swopy import swop, systems
from swopy.systems._algorithms import (
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    longest_match_from_numeral,
    multiplicative_additive_from_numeral,
    multiplicative_additive_to_numeral,
    multiplicative_myriad_from_numeral,
    multiplicative_myriad_to_numeral,
    positional_to_numeral,
    reversed_greedy_additive_to_numeral,
    subtractive_to_numeral,
)


class TestRomanStandard:
    """
    Specific tests for systems.roman.Standard
    """

    def test_double_half(self) -> None:
        """
        Checks that a value error is raised when two incompatible
        fraction characters are used
        """
        with pytest.raises(ValueError):
            systems.roman.Standard.from_numeral("SS")

    def test_not_base_12_fraction(self) -> None:
        """
        Checks that a value error is raised when the fraction for
        roman.Standard is not base 12.
        """
        with pytest.raises(ValueError):
            systems.roman.Standard.to_numeral(Fraction(1, 7))


class TestRomanApostrophus:
    """
    Specific tests for systems.roman.Apostrophus
    """

    def test_incorrect_character_order(self) -> None:
        """
        Checks that a value error is raised when valid characters
        in an invalid order are used.
        """
        with pytest.raises(ValueError):
            systems.roman.Apostrophus.from_numeral("ⅠⅠↃⅠ")


class TestGreekEtruscan:
    """Specific tests for systems.greek.Etruscan."""

    def test_to_numeral_four(self):
        # 4 = 4×1; Etruscan has no subtractive notation
        assert systems.greek.Etruscan.to_numeral(4) == "\U00010320" * 4

    def test_to_numeral_six(self):
        # 6 = 1 + 5; RTL → smallest on the left: 𐌠𐌡
        assert systems.greek.Etruscan.to_numeral(6) == "\U00010320" + "\U00010321"

    def test_to_numeral_seventeen(self):
        # 17 = 2×1 + 1×5 + 1×10; RTL: 𐌠𐌠𐌡𐌢
        assert (
            systems.greek.Etruscan.to_numeral(17)
            == "\U00010320" * 2 + "\U00010321" + "\U00010322"
        )

    def test_to_numeral_twentynine(self):
        # 29 = 4×1 + 1×5 + 2×10; RTL: 𐌠𐌠𐌠𐌠𐌡𐌢𐌢
        assert (
            systems.greek.Etruscan.to_numeral(29)
            == "\U00010320" * 4 + "\U00010321" + "\U00010322" * 2
        )


class TestKharosthiKharosthi:
    """Specific tests for systems.kharosthi.Kharosthi"""

    def test_to_numeral(self):
        # 2+4+10+20+20+20+20 + 100x(1+4+4) + 1000
        assert systems.kharosthi.Kharosthi.to_numeral(1996) == "𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁"

    @staticmethod
    def _units_str_reference(n: int, m: Mapping[int, str]) -> str:
        """Verbatim copy of the original _units_str for regression testing."""
        result = ""
        for value in (4, 3, 2, 1):
            result += m[value] * (n // value)
            n %= value
        return result

    @given(strategies.integers(min_value=0, max_value=9))
    def test_units_str_matches_reference(self, n: int) -> None:
        """_units_str must match the reference loop implementation."""
        m = systems.kharosthi.Kharosthi._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert (
            systems.kharosthi.Kharosthi._units_str(n)  # pyright: ignore[reportPrivateUsage]
            == self._units_str_reference(n, m)
        )


class TestGreekAttic:
    """Specific tests for systems.greek.Attic."""

    def test_non_representable_fraction(self) -> None:
        """Checks that a ValueError is raised for a fraction that cannot be
        represented in Attic numerals (only 1/2 and 1/4 are supported).
        """
        with pytest.raises(ValueError):
            systems.greek.Attic.to_numeral(Fraction(1, 3))


class TestKaktovik:
    """Specific tests for systems.kaktovik.Kaktovik."""

    def test_42(self) -> None:
        """Checks that 42 encodes as two Kaktovik twos (2×20 + 2)."""
        assert systems.kaktovik.Kaktovik.to_numeral(42) == "\U0001d2c2\U0001d2c2"

    def test_negative(self) -> None:
        """Checks that negative integers are prefixed with a hyphen-minus."""
        assert systems.kaktovik.Kaktovik.to_numeral(-1) == "-\U0001d2c1"
        assert systems.kaktovik.Kaktovik.from_numeral("-\U0001d2c1") == -1

    def test_large_number(self) -> None:
        """Checks that numbers greater than 10^20 round-trip correctly."""
        n = 10**21
        assert (
            systems.kaktovik.Kaktovik.from_numeral(
                systems.kaktovik.Kaktovik.to_numeral(n)
            )
            == n
        )

    def test_bare_hyphen_raises(self) -> None:
        """Checks that a lone hyphen-minus raises ValueError."""
        with pytest.raises(ValueError, match="Invalid Kaktovik numeral"):
            systems.kaktovik.Kaktovik.from_numeral("-")


class TestAramaicImperialAramaic:
    """Specific tests for systems.aramaic.ImperialAramaic."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.aramaic.ImperialAramaic.to_numeral(1001)
        assert numeral[-1] == "\U0001085e"  # ONE THOUSAND on right


class TestSogdianManichaean:
    """Specific tests for systems.sogdian.Manichaean."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.sogdian.Manichaean.to_numeral(11)
        assert numeral[-1] == "\U00010aed"  # TEN on right


class TestSogdianOldSogdian:
    """Specific tests for systems.sogdian.OldSogdian."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.sogdian.OldSogdian.to_numeral(101)
        assert numeral[-1] == "\U00010f25"  # ONE HUNDRED on right


class TestSogdianSogdian:
    """Specific tests for systems.sogdian.Sogdian."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.sogdian.Sogdian.to_numeral(21)
        assert numeral[-1] == "\U00010f53"  # TWENTY on right


class TestSouthArabianAncientSouthArabian:
    """Specific tests for systems.south_arabian.AncientSouthArabian"""

    def test_to_numeral(self):
        assert systems.south_arabian.AncientSouthArabian.to_numeral(31000) == "𐩲𐩲𐩲𐩱"
        assert systems.south_arabian.AncientSouthArabian.to_numeral(40000) == "𐩲𐩲𐩲𐩲"


class TestPahlaviInscriptionalParthian:
    """Specific tests for systems.pahlavi.InscriptionalParthian."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.pahlavi.InscriptionalParthian.to_numeral(1001)
        assert numeral[-1] == "\U00010b5f"  # ONE THOUSAND on right

    def test_round_trip(self) -> None:
        """Checks a representative value round-trips correctly."""
        assert (
            systems.pahlavi.InscriptionalParthian.from_numeral(
                systems.pahlavi.InscriptionalParthian.to_numeral(9999)
            )
            == 9999  # noqa: PLR2004
        )


class TestPahlaviInscriptionalPahlavi:
    """Specific tests for systems.pahlavi.InscriptionalPahlavi."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.pahlavi.InscriptionalPahlavi.to_numeral(1001)
        assert numeral[-1] == "\U00010b7f"  # ONE THOUSAND on right


class TestPahlaviPsalterPahlavi:
    """Specific tests for systems.pahlavi.PsalterPahlavi."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.pahlavi.PsalterPahlavi.to_numeral(101)
        assert numeral[-1] == "\U00010baf"  # ONE HUNDRED on right


class TestSiyaqOttomanSiyaq:
    """Specific tests for systems.siyaq.OttomanSiyaq."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.siyaq.OttomanSiyaq.to_numeral(11)
        assert numeral[-1] == "\U0001ed0a"  # TEN on right

    def test_alternate_forms_accepted(self) -> None:
        """Checks that alternate glyph forms decode to the correct value."""
        assert systems.siyaq.OttomanSiyaq.from_numeral("\U0001ed2f") == 2  # noqa: PLR2004
        assert systems.siyaq.OttomanSiyaq.from_numeral("\U0001ed3b") == 10000  # noqa: PLR2004


class TestSiyaqIndicSiyaq:
    """Specific tests for systems.siyaq.IndicSiyaq."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.siyaq.IndicSiyaq.to_numeral(11)
        assert numeral[-1] == "\U0001ec7a"  # TEN on right

    def test_alternate_forms_accepted(self) -> None:
        """Checks that alternate and prefixed glyph forms decode correctly."""
        assert systems.siyaq.IndicSiyaq.from_numeral("\U0001eca3") == 1
        assert systems.siyaq.IndicSiyaq.from_numeral("\U0001ecb3") == 10000  # noqa: PLR2004


class TestBrahmiGuptaSinhalaArchaic:
    """Specific tests for systems.brahmi_gupta.SinhalaArchaic."""

    def test_multiplicative_hundreds(self) -> None:
        """Checks that hundreds use a unit multiplier glyph."""
        assert systems.brahmi_gupta.SinhalaArchaic.to_numeral(200) == (
            "\U000111e2\U000111f3"
        )

    def test_round_trip(self) -> None:
        """Checks a representative value round-trips correctly."""
        assert (
            systems.brahmi_gupta.SinhalaArchaic.from_numeral(
                systems.brahmi_gupta.SinhalaArchaic.to_numeral(1996)
            )
            == 1996  # noqa: PLR2004
        )


class TestBrahmiGuptaBhaiksuki:
    """Specific tests for systems.brahmi_gupta.Bhaiksuki."""

    def test_hundreds_compound_glyph(self) -> None:
        """Checks that hundreds are encoded as unit-sign + hundreds-mark."""
        result = systems.brahmi_gupta.Bhaiksuki.to_numeral(100)
        assert result == "\U00011c5a\U00011c6c"  # ONE + HUNDREDS MARK

    def test_compound_decodes_correctly(self) -> None:
        """Checks that compound hundred tokens decode without ambiguity."""
        assert (
            systems.brahmi_gupta.Bhaiksuki.from_numeral("\U00011c5a\U00011c6c") == 100  # noqa: PLR2004
        )
        assert (
            systems.brahmi_gupta.Bhaiksuki.from_numeral("\U00011c62\U00011c6c") == 900  # noqa: PLR2004
        )


class TestBrahmiTaiAhom:
    """Specific tests for systems.brahmi_tai.Ahom."""

    def test_positional_encoding(self) -> None:
        """Checks that 42 encodes as Ahom digit 4 followed by digit 2."""
        assert systems.brahmi_tai.Ahom.to_numeral(42) == "\U00011734\U00011732"

    def test_ten_sign_accepted(self) -> None:
        """Checks that the dedicated ten sign (U+1173A) is accepted as input."""
        assert systems.brahmi_tai.Ahom.from_numeral("\U0001173a") == 10  # noqa: PLR2004


class TestMedefaidrinMedefaidrin:
    """Specific tests for systems.medefaidrin.Medefaidrin."""

    def test_42(self) -> None:
        """Checks that 42 encodes as two Medefaidrin twos (2×20 + 2)."""
        assert systems.medefaidrin.Medefaidrin.to_numeral(42) == "\U00016e82\U00016e82"

    def test_alternate_forms_accepted(self) -> None:
        """Checks that alternate digit forms for 1-3 are accepted as input."""
        assert systems.medefaidrin.Medefaidrin.from_numeral("\U00016e94") == 1
        assert systems.medefaidrin.Medefaidrin.from_numeral("\U00016e96") == 3  # noqa: PLR2004


class TestSinoTibetanSuzhou:
    """Specific tests for systems.sino_tibetan.Suzhou."""

    def test_shorthand_standalone(self) -> None:
        """Checks that standalone shorthand glyphs decode to 10, 20, and 30."""
        assert systems.sino_tibetan.Suzhou.from_numeral("\u3038") == 10  # noqa: PLR2004  # 〸
        assert systems.sino_tibetan.Suzhou.from_numeral("\u3039") == 20  # noqa: PLR2004  # 〹
        assert systems.sino_tibetan.Suzhou.from_numeral("\u303a") == 30  # noqa: PLR2004  # 〺

    def test_shorthand_mid_string_raises(self) -> None:
        """Checks that a shorthand glyph (〸/〹/〺) inside a longer string raises."""
        with pytest.raises(ValueError, match="Invalid Suzhou character"):
            systems.sino_tibetan.Suzhou.from_numeral("\u3038\u3021")  # 〸〡


class TestSwop:
    """Regression tests for swopy.swop() behaviour."""

    def test_incompatible_type_raises_type_error(self) -> None:
        """Checks that swop() raises TypeError when the intermediate value is
        incompatible with the target system's denotation type.

        Roman Standard produces Fraction values (e.g. S = 1/2). Mayan only
        accepts integers. Swapping from Standard to Mayan for a fractional
        numeral must raise TypeError.
        """
        with pytest.raises(TypeError):
            swop("S", systems.roman.Standard, systems.mayan.Mayan)


class TestEthiopicEthiopic:
    """Specific tests for systems.ethiopic.Ethiopic."""

    def test_myriad_no_remainder(self) -> None:
        """Checks that exact multiples of 10,000 round-trip correctly.

        Exercises the empty-string branch of _decode_sub9999 (line 93 of
        ethiopic.py), which returns 0 when the myriad glyph is the last
        character and there is no trailing remainder segment.
        """
        assert systems.ethiopic.Ethiopic.from_numeral("\u137c") == 10000  # noqa: PLR2004
        assert systems.ethiopic.Ethiopic.from_numeral("\u136a\u137c") == 20000  # noqa: PLR2004


class TestAlgorithmsGreedyAdditive:
    """Checks that any new greedy_additive_to_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.

    The reference accepts a Mapping and calls .items() internally.  The live
    function now accepts a pre-computed items sequence (tuple of pairs) so tests
    pass ``tuple(m.items())`` to bridge the two APIs while keeping the reference
    unchanged.
    """

    @staticmethod
    def _reference(number: int, numeral_map: Mapping[int, str]) -> str:
        result: str = ""
        for value, glyph in numeral_map.items():
            count, number = divmod(number, value)
            result += glyph * count
        return result

    @given(strategies.integers(min_value=1, max_value=999_999))
    def test_egyptian(self, number: int) -> None:
        """Egyptian map: powers of 10 up to 1,000,000 — exercises large counts."""
        m = systems.egyptian.Egyptian.to_numeral_map()
        assert greedy_additive_to_numeral(number, tuple(m.items())) == self._reference(
            number, m
        )

    @given(strategies.integers(min_value=1, max_value=999))
    def test_nabataean(self, number: int) -> None:
        """Nabataean map: non-power-of-10 denominations — exercises sparse glyphs."""
        m = systems.nabataean.Nabataean.to_numeral_map()
        assert greedy_additive_to_numeral(number, tuple(m.items())) == self._reference(
            number, m
        )

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_reversed_pahlavi(self, number: int) -> None:
        """InscriptionalParthian — exercises the reversed (RTL) variant."""
        m = systems.pahlavi.InscriptionalParthian.to_numeral_map()
        assert (
            reversed_greedy_additive_to_numeral(number, tuple(m.items()))
            == self._reference(number, m)[::-1]
        )

    @given(strategies.integers(min_value=1, max_value=99_999))
    def test_ottoman_siyaq(self, number: int) -> None:
        """OttomanSiyaq map: 45 entries — exercises large-map systems where
        leading denominations exceed the input value on most calls."""
        m = systems.siyaq.OttomanSiyaq.to_numeral_map()
        assert greedy_additive_to_numeral(number, tuple(m.items())) == self._reference(
            number, m
        )


class TestAlgorithmsLongestMatch:
    """Checks that any new longest_match_from_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(  # noqa: PLR0913
        numeral: str,
        from_map: Mapping[str, int],
        system_name: str,
        *,
        case_fold: bool = False,
        enforce_descending: bool = False,
        initial_max: int | None = None,
    ) -> int:
        if case_fold:
            numeral = numeral.upper()

        last_value: int = (
            (initial_max if initial_max is not None else max(from_map.values()) + 1)
            if enforce_descending
            else 0
        )

        total = 0
        i = 0
        while i < len(numeral):
            matched = False
            for symbol, value in from_map.items():
                if numeral.startswith(symbol, i):
                    if enforce_descending and value > last_value:
                        raise ValueError(
                            f"Invalid {system_name} sequence: {symbol!r} cannot"
                            " follow a smaller value."
                        )
                    total += value
                    last_value = value
                    i += len(symbol)
                    matched = True
                    break

            if not matched:
                raise ValueError(
                    f"Invalid {system_name} character at position {i}: {numeral[i]!r}"
                )

        return total

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_hebrew(self, number: int) -> None:
        """Hebrew map: 37 entries, default options."""
        numeral = systems.hebrew.Hebrew.to_numeral(number)
        m = systems.hebrew.Hebrew._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert longest_match_from_numeral(numeral, m, "Hebrew") == self._reference(
            numeral, m, "Hebrew"
        )

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_greek_milesian(self, number: int) -> None:
        """Greek Milesian map: 72 entries — largest map, exercises the hot path."""
        numeral = systems.greek.Milesian.to_numeral(number)
        m = systems.greek.Milesian._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert longest_match_from_numeral(numeral, m, "Milesian") == self._reference(
            numeral, m, "Milesian"
        )

    @given(strategies.integers(min_value=1, max_value=100_000))
    def test_roman_apostrophus(self, number: int) -> None:
        """Roman Apostrophus: case_fold + enforce_descending + multi-char tokens."""
        numeral = systems.roman.Apostrophus.to_numeral(number)
        m = systems.roman.Apostrophus._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert longest_match_from_numeral(
            numeral, m, "Apostrophus", case_fold=True, enforce_descending=True
        ) == self._reference(
            numeral, m, "Apostrophus", case_fold=True, enforce_descending=True
        )


class TestAlgorithmsMultiplicativeAdditive:
    """Checks multiplicative_additive_from_numeral against the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as
    it existed before any optimisation.  These tests should remain unchanged so
    that future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(numeral: str, from_map: Mapping[str, int], system_name: str) -> int:
        unit_glyphs = frozenset(g for g, v in from_map.items() if 1 <= v <= 9)  # noqa: PLR2004
        multiplier_glyphs = {g: v for g, v in from_map.items() if v in {100, 1000}}
        decade_glyphs = {g: v for g, v in from_map.items() if 10 <= v <= 90}  # noqa: PLR2004

        total = 0
        unit_buffer = 0

        for char in numeral:
            if char not in from_map:
                raise ValueError(f"Invalid {system_name} character: {char!r}")

            if char in unit_glyphs:
                unit_buffer += from_map[char]
            elif char in multiplier_glyphs:
                total += multiplier_glyphs[char] * max(unit_buffer, 1)
                unit_buffer = 0
            else:
                total += unit_buffer
                unit_buffer = 0
                total += decade_glyphs[char]

        total += unit_buffer
        return total

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_sinhala_archaic(self, number: int) -> None:
        """SinhalaArchaic: thousands/hundreds/tens/units — multiplicative-additive."""
        numeral = systems.brahmi_gupta.SinhalaArchaic.to_numeral(number)
        m = systems.brahmi_gupta.SinhalaArchaic._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        got = multiplicative_additive_from_numeral(numeral, m, "SinhalaArchaic")
        assert got == self._reference(numeral, m, "SinhalaArchaic")

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_kharosthi(self, number: int) -> None:
        """Kharosthi: exercises a different glyph set for the same algorithm."""
        numeral = systems.kharosthi.Kharosthi.to_numeral(number)
        m = systems.kharosthi.Kharosthi._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        got = multiplicative_additive_from_numeral(numeral, m, "Kharosthi")
        assert got == self._reference(numeral, m, "Kharosthi")


class TestAlgorithmsMultiplicativeAdditiveTo:
    """Checks any new multiplicative_additive_to_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int, numeral_map: Mapping[int, str]) -> str:
        result = ""

        thousands, number = divmod(number, 1000)
        if thousands:
            if thousands > 1:
                result += numeral_map[thousands]
            result += numeral_map[1000]

        hundreds, number = divmod(number, 100)
        if hundreds:
            if hundreds > 1:
                result += numeral_map[hundreds]
            result += numeral_map[100]

        tens, number = divmod(number, 10)
        if tens:
            result += numeral_map[tens * 10]

        if number:
            result += numeral_map[number]

        return result

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_sinhala_archaic(self, number: int) -> None:
        """SinhalaArchaic: twenty-glyph map — canonical multiplicative-additive caller."""  # noqa: E501
        m = systems.brahmi_gupta.SinhalaArchaic.to_numeral_map()
        assert multiplicative_additive_to_numeral(number, m) == self._reference(
            number, m
        )

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_brahmi(self, number: int) -> None:
        """Brahmi: different glyph set, same algorithm structure."""
        m = systems.brahmi.Brahmi.to_numeral_map()
        assert multiplicative_additive_to_numeral(number, m) == self._reference(
            number, m
        )

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_bakhshali(self, number: int) -> None:
        """Bakhshali: third caller — exercises the same code path with a third glyph set."""  # noqa: E501
        m = systems.hindu_arabic.Bakhshali.to_numeral_map()
        assert multiplicative_additive_to_numeral(number, m) == self._reference(
            number, m
        )


class TestAlgorithmsCharSum:
    """Checks that any new char_sum_from_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(numeral: str, from_map: Mapping[str, int], system_name: str) -> int:
        total: int = 0
        for char in numeral:
            if char not in from_map:
                raise ValueError(f"Invalid {system_name} character: {char!r}")
            total += from_map[char]
        return total

    @given(strategies.integers(min_value=1, max_value=999_999))
    def test_egyptian(self, number: int) -> None:
        """Egyptian: powers-of-10 map up to 1,000,000 — large additive sums."""
        numeral = systems.egyptian.Egyptian.to_numeral(number)
        m = systems.egyptian.Egyptian._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert char_sum_from_numeral(numeral, m, "Egyptian") == self._reference(
            numeral, m, "Egyptian"
        )

    @given(strategies.integers(min_value=1, max_value=999))
    def test_nabataean(self, number: int) -> None:
        """Nabataean: non-power-of-10 denominations — exercises sparse glyph sums."""
        numeral = systems.nabataean.Nabataean.to_numeral(number)
        m = systems.nabataean.Nabataean._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert char_sum_from_numeral(numeral, m, "Nabataean") == self._reference(
            numeral, m, "Nabataean"
        )


class TestAlgorithmsPositionalTo:
    """Checks that any new positional_to_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int, to_map: Mapping[int, str], base: int) -> str:
        if number == 0:
            return to_map[0]
        parts: list[str] = []
        while number:
            number, remainder = divmod(number, base)
            parts.append(to_map[remainder])
        return "".join(reversed(parts))

    @given(strategies.integers(min_value=0, max_value=1_000_000))
    def test_kaktovik(self, number: int) -> None:
        """Kaktovik: base-20 vigesimal — exercises multi-digit positional encoding."""
        m = systems.kaktovik.Kaktovik._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert positional_to_numeral(number, m, 20) == self._reference(number, m, 20)

    @given(strategies.integers(min_value=0, max_value=8000))
    def test_mayan(self, number: int) -> None:
        """Mayan: base-20 — different glyph set, same algorithm."""
        m = systems.mayan.Mayan._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert positional_to_numeral(number, m, 20) == self._reference(number, m, 20)


class TestAlgorithmsMyriad:
    """Checks multiplicative_myriad_from_numeral against the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as
    it existed before any optimisation.  These tests should remain unchanged so
    that future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(
        numeral: str,
        digit_map: Mapping[str, int],
        multiplier_map: Mapping[str, int],
        system_name: str,
    ) -> int:
        _myriad = 10000
        myriad_glyph = next(g for g, v in multiplier_map.items() if v == _myriad)
        sub_mult_map = {g: v for g, v in multiplier_map.items() if v != _myriad}

        def parse_sub(s: str) -> int:
            total = 0
            i = 0
            while i < len(s):
                c = s[i]
                if c in digit_map:
                    digit = digit_map[c]
                    i += 1
                    if i < len(s) and s[i] in sub_mult_map:
                        total += digit * sub_mult_map[s[i]]
                        i += 1
                    else:
                        total += digit
                elif c in sub_mult_map:
                    total += sub_mult_map[c]
                    i += 1
                else:
                    raise ValueError(f"Invalid {system_name} character: {c!r}")
            return total

        if myriad_glyph in numeral:
            idx = numeral.index(myriad_glyph)
            coeff = parse_sub(numeral[:idx]) if idx > 0 else 1
            remainder = parse_sub(numeral[idx + 1 :]) if idx + 1 < len(numeral) else 0
            return coeff * 10000 + remainder
        return parse_sub(numeral)

    @given(strategies.integers(min_value=1, max_value=99_999_999))
    def test_tangut(self, number: int) -> None:
        """Tangut: explicit-one-tens, max 99,999,999 — exercises the myriad split."""
        numeral = systems.sino_tibetan.Tangut.to_numeral(number)
        dm = systems.sino_tibetan.Tangut._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        mm = systems.sino_tibetan.Tangut._multiplier_from_map  # pyright: ignore[reportPrivateUsage]
        got = multiplicative_myriad_from_numeral(numeral, dm, mm, "Tangut")
        assert got == self._reference(numeral, dm, mm, "Tangut")

    @given(strategies.integers(min_value=1, max_value=99_999_999))
    def test_khitan(self, number: int) -> None:
        """Khitan: no explicit-one-tens — exercises the implicit-one variant."""
        numeral = systems.sino_tibetan.Khitan.to_numeral(number)
        dm = systems.sino_tibetan.Khitan._from_numeral_map  # pyright: ignore[reportPrivateUsage]
        mm = systems.sino_tibetan.Khitan._multiplier_from_map  # pyright: ignore[reportPrivateUsage]
        got = multiplicative_myriad_from_numeral(numeral, dm, mm, "Khitan")
        assert got == self._reference(numeral, dm, mm, "Khitan")


class TestAlgorithmsMyriadTo:
    """Checks multiplicative_myriad_to_numeral against the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as
    it existed before any optimisation.  These tests should remain unchanged so
    that future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(
        number: int,
        digit_map: Mapping[int, str],
        multiplier_map: Mapping[int, str],
        *,
        explicit_one_tens: bool = False,
    ) -> str:
        _myriad = 10000
        _ten = 10
        myriad_glyph = multiplier_map[_myriad]
        sub_mult = [(k, v) for k, v in multiplier_map.items() if k != _myriad]

        def encode_sub(n: int) -> str:
            res = ""
            for mult, glyph in sub_mult:
                coeff, n = divmod(n, mult)
                if coeff:
                    if coeff > 1 or (explicit_one_tens and mult == _ten):
                        res += digit_map[coeff]
                    res += glyph
            if n:
                res += digit_map[n]
            return res

        myriads, remainder = divmod(number, _myriad)
        result = ""
        if myriads:
            if myriads > 1 or explicit_one_tens:
                result += encode_sub(myriads)
            result += myriad_glyph
        if remainder:
            result += encode_sub(remainder)
        return result

    @given(strategies.integers(min_value=1, max_value=99_999_999))
    def test_tangut(self, number: int) -> None:
        """Tangut: explicit-one-tens — exercises the myriad split and sub-encoding."""
        dm = systems.sino_tibetan.Tangut._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        mm = systems.sino_tibetan.Tangut._multiplier_map  # pyright: ignore[reportPrivateUsage]
        assert multiplicative_myriad_to_numeral(
            number, dm, mm, explicit_one_tens=True
        ) == self._reference(number, dm, mm, explicit_one_tens=True)

    @given(strategies.integers(min_value=1, max_value=99_999_999))
    def test_khitan(self, number: int) -> None:
        """Khitan: no explicit-one-tens — exercises the implicit-one variant."""
        dm = systems.sino_tibetan.Khitan._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        mm = systems.sino_tibetan.Khitan._multiplier_map  # pyright: ignore[reportPrivateUsage]
        assert multiplicative_myriad_to_numeral(number, dm, mm) == self._reference(
            number, dm, mm
        )


class TestAlgorithmsSubtractiveTo:
    """Checks that any new subtractive_to_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as
    it existed before any optimisation.  These tests should remain unchanged so
    that future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int | Fraction, numeral_map: Mapping[Any, str]) -> str:
        result = ""
        for value, glyph in numeral_map.items():
            while number >= value:
                result += glyph
                number -= value
        return result

    @given(strategies.integers(min_value=1, max_value=3999))
    def test_roman_standard_integers(self, number: int) -> None:
        """Roman Standard: integer inputs exercise the integer portion of the map
        and confirm early termination does not affect the result.
        """
        m = systems.roman.Standard.to_numeral_map()
        assert subtractive_to_numeral(number, m) == self._reference(number, m)  # type: ignore[arg-type]

    @given(
        strategies.fractions(
            min_value=Fraction(1, 12),
            max_value=Fraction(11, 12),
            max_denominator=12,
        )
    )
    def test_roman_standard_fractions(self, number: Fraction) -> None:
        """Roman Standard: fractional inputs exercise the Fraction tail of the map."""
        m = systems.roman.Standard.to_numeral_map()
        assert (  # type: ignore[arg-type]
            subtractive_to_numeral(number, m)  # type: ignore[arg-type]
            == self._reference(number, m)
        )


class TestRomanStandardToNumeralLoop:
    """Regression tests for the roman.Standard._to_numeral inline loop.

    The reference below is a verbatim copy of the _to_numeral implementation
    before any optimisation.  These tests should remain unchanged so that future
    rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int | Fraction) -> str:
        result: str = ""
        integer = int(number)
        proper_fraction = abs(int(number) - number)
        for arabic, roman in systems.roman.Standard.to_numeral_map().items():
            while integer >= arabic:
                result += roman
                integer -= arabic
        if proper_fraction == 0:
            return result
        try:
            result += systems.roman.Standard.to_numeral_map()[proper_fraction]
        except KeyError as e:
            raise ValueError(f"{number} cannot be represented in Standard.") from e
        return result

    @given(strategies.integers(min_value=1, max_value=3999))
    def test_integers(self, number: int) -> None:
        """Integer inputs: confirm that an early break at integer==0 does not
        affect output, covering values where the Fraction tail would otherwise
        be iterated.
        """
        assert systems.roman.Standard.to_numeral(number) == self._reference(number)

    # Fractions representable as a single Roman uncia glyph
    _VALID_FRACTIONS: ClassVar[list[Fraction]] = [
        k for k in systems.roman.Standard.to_numeral_map() if isinstance(k, Fraction)
    ]

    @given(strategies.sampled_from(_VALID_FRACTIONS))
    def test_proper_fractions(self, number: Fraction) -> None:
        """Pure fractional inputs: integer part is zero so the break fires
        immediately; the fraction glyph must still be looked up correctly.
        """
        assert systems.roman.Standard.to_numeral(number) == self._reference(number)

    @given(
        strategies.integers(min_value=1, max_value=3998),
        strategies.sampled_from(_VALID_FRACTIONS),
    )
    def test_mixed(self, integer: int, frac: Fraction) -> None:
        """Mixed integer+fraction inputs: both the integer and fractional
        glyphs must be produced correctly after early break.
        """
        number = Fraction(integer) + frac
        assert systems.roman.Standard.to_numeral(number) == self._reference(number)


class TestGreekAtticToNumeral:
    """Regression tests for greek.Attic._to_numeral.

    The reference below is a verbatim copy of the _to_numeral implementation
    before any optimisation.  These tests should remain unchanged so that future
    rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int | Fraction) -> str:
        n = Fraction(number)
        integer_part = int(n)
        frac_part = n - integer_part
        result = ""
        for value, glyph in systems.greek.Attic._to_numeral_map.items():  # pyright: ignore[reportPrivateUsage]
            if isinstance(value, Fraction):
                continue
            count, integer_part = divmod(integer_part, value)
            result += glyph * count
        if frac_part >= Fraction(1, 2):
            result += systems.greek.Attic._to_numeral_map[Fraction(1, 2)]  # pyright: ignore[reportPrivateUsage]
            frac_part -= Fraction(1, 2)
        if frac_part >= Fraction(1, 4):
            result += systems.greek.Attic._to_numeral_map[Fraction(1, 4)]  # pyright: ignore[reportPrivateUsage]
            frac_part -= Fraction(1, 4)
        if frac_part:
            raise ValueError(f"{number} cannot be represented in Attic.")
        return result

    @given(strategies.integers(min_value=1, max_value=99999))
    def test_integers(self, number: int) -> None:
        """Integer inputs: the common case — confirm no Fraction construction
        changes the result.
        """
        assert systems.greek.Attic.to_numeral(number) == self._reference(number)

    @given(strategies.sampled_from([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]))
    def test_pure_fractions(self, number: Fraction) -> None:
        """Pure fractional inputs (1/4, 1/2, 3/4): integer part is zero."""
        assert systems.greek.Attic.to_numeral(number) == self._reference(number)

    @given(
        strategies.integers(min_value=1, max_value=99998),
        strategies.sampled_from([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]),
    )
    def test_mixed(self, integer: int, frac: Fraction) -> None:
        """Mixed integer+fraction inputs: both parts must be encoded correctly."""
        number = Fraction(integer) + frac
        assert systems.greek.Attic.to_numeral(number) == self._reference(number)


class TestEthiopicToNumeral:
    """Regression tests for ethiopic.Ethiopic._to_numeral (and _encode_sub9999).

    The reference below is a verbatim copy of the implementation before the
    divmod -> // / % optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference_encode_sub9999(n: int) -> str:
        _encode_sub100 = systems.ethiopic._encode_sub100  # pyright: ignore[reportPrivateUsage]
        result = ""
        hundreds, remainder = divmod(n, 100)
        if hundreds:
            if hundreds != 1:
                result += _encode_sub100(hundreds)
            result += "\u137b"
        result += _encode_sub100(remainder) if remainder else ""
        return result

    @staticmethod
    def _reference(number: int) -> str:
        _encode_sub9999 = systems.ethiopic._encode_sub9999  # pyright: ignore[reportPrivateUsage]
        myriads, remainder = divmod(number, 10000)
        result = ""
        if myriads:
            if myriads != 1:
                result += _encode_sub9999(myriads)
            result += "\u137c"
        result += _encode_sub9999(remainder) if remainder else ""
        return result

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_sub9999(self, number: int) -> None:
        """Sub-myriad range: exercises the hundreds divmod in _encode_sub9999."""
        assert systems.ethiopic.Ethiopic.to_numeral(
            number
        ) == self._reference_encode_sub9999(number)

    @given(strategies.integers(min_value=10000, max_value=99_999_999))
    def test_myriad(self, number: int) -> None:
        """Myriad range: exercises the top-level divmod in Ethiopic._to_numeral."""
        assert systems.ethiopic.Ethiopic.to_numeral(number) == self._reference(number)


class TestTamilToNumeral:
    """Regression tests for brahmi_dravidian.Tamil._to_numeral.

    The reference below is a verbatim copy of the implementation before the
    divmod -> // / % optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
    """

    @staticmethod
    def _reference(number: int) -> str:
        dm = systems.brahmi_dravidian.Tamil._digit_map  # pyright: ignore[reportPrivateUsage]
        mm = systems.brahmi_dravidian.Tamil._multiplier_map  # pyright: ignore[reportPrivateUsage]
        result = ""
        for mult in [1000, 100, 10]:
            coeff, number = divmod(number, mult)
            if coeff:
                if coeff > 1:
                    result += dm[coeff]
                result += mm[mult]
        if number:
            result += dm[number]
        return result

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_integers(self, number: int) -> None:
        """Full valid range — exercises all multiplier tiers."""
        assert systems.brahmi_dravidian.Tamil.to_numeral(number) == self._reference(
            number
        )


class TestLimitsBounded:
    """Regression tests for the _bounded short-circuit in System._limits().

    The reference below replicates the original _limits logic (without the
    _bounded flag) so that any change to the fast path can be validated.
    """

    @staticmethod
    def _reference(system: Any, number: Any) -> Any:
        number_ = number
        minimum = system.minimum
        maximum = system.maximum
        if number_ < minimum:
            raise ValueError(f"Number must be greater or equal to {minimum}.")
        if system.maximum_is_many and number_ > maximum:
            return maximum
        if number_ > maximum:
            raise ValueError(f"Number must be less than or equal to {maximum}.")
        return number_

    @given(strategies.integers())
    def test_arabic_unbounded(self, number: int) -> None:
        """Arabic has minimum=-inf, maximum=inf: _limits must be a no-op."""
        assert systems.hindu_arabic.Arabic._bounded is False  # pyright: ignore[reportPrivateUsage]
        assert systems.hindu_arabic.Arabic._limits(number) == self._reference(  # pyright: ignore[reportPrivateUsage]
            systems.hindu_arabic.Arabic, number
        )

    @given(strategies.integers(min_value=1, max_value=3999))
    def test_roman_standard_in_range(self, number: int) -> None:
        """Roman Standard is bounded; in-range inputs must pass through unchanged."""
        assert systems.roman.Standard._bounded is True  # pyright: ignore[reportPrivateUsage]
        assert systems.roman.Standard._limits(number) == self._reference(  # pyright: ignore[reportPrivateUsage]
            systems.roman.Standard, number
        )

    def test_roman_standard_below_minimum_raises(self) -> None:
        """Roman Standard: values below minimum must still raise ValueError."""
        with pytest.raises(ValueError, match="greater or equal"):
            systems.roman.Standard._limits(0)  # pyright: ignore[reportPrivateUsage]

    def test_roman_standard_above_maximum_raises(self) -> None:
        """Roman Standard: values above maximum must still raise ValueError."""
        with pytest.raises(ValueError, match="less than or equal"):
            systems.roman.Standard._limits(4000)  # pyright: ignore[reportPrivateUsage]


class TestFromNumeralTrusted:
    """Regression tests for System.from_numeral_trusted().

    Verifies that from_numeral_trusted() produces the same denotation as
    from_numeral() for all valid inputs.  The trusted variant omits the
    is_valid_numeral guard; these tests confirm that removing the guard does
    not alter the result on well-typed inputs.
    """

    @given(strategies.integers(min_value=1, max_value=3999))
    def test_roman_standard_integers(self, number: int) -> None:
        """Roman Standard: integer round-trip — covers the common int path."""
        numeral = systems.roman.Standard.to_numeral(number)
        assert systems.roman.Standard.from_numeral_trusted(numeral) == (
            systems.roman.Standard.from_numeral(numeral)
        )

    @given(strategies.integers(min_value=1, max_value=99_999))
    def test_ottoman_siyaq(self, number: int) -> None:
        """OttomanSiyaq: large map — confirms trusted path is correct for
        systems with many denominations."""
        numeral = systems.siyaq.OttomanSiyaq.to_numeral(number)
        assert systems.siyaq.OttomanSiyaq.from_numeral_trusted(numeral) == (
            systems.siyaq.OttomanSiyaq.from_numeral(numeral)
        )

    @given(strategies.integers(min_value=1, max_value=99_999))
    def test_greek_aegean(self, number: int) -> None:
        """Greek Aegean: 45-entry map, UTF-8 multi-char glyphs."""
        numeral = systems.greek.Aegean.to_numeral(number)
        assert systems.greek.Aegean.from_numeral_trusted(numeral) == (
            systems.greek.Aegean.from_numeral(numeral)
        )


class TestToNumeralItems:
    """Regression tests verifying that _to_numeral_items matches
    _to_numeral_map.items().

    The _to_numeral_items ClassVar is pre-computed in __init_subclass__ and passed
    directly to greedy_additive_to_numeral, bypassing the per-call .items() view
    allocation.  These tests confirm the pre-computed data is correct.
    """

    def test_roman_standard_items_match_map(self) -> None:
        """roman.Standard: 24-entry map with int and Fraction keys."""
        m = systems.roman.Standard._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert tuple(m.items()) == systems.roman.Standard._to_numeral_items  # pyright: ignore[reportPrivateUsage]

    def test_ottoman_siyaq_items_match_map(self) -> None:
        """OttomanSiyaq: 45-entry map — largest standard greedy map."""
        m = systems.siyaq.OttomanSiyaq._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert tuple(m.items()) == systems.siyaq.OttomanSiyaq._to_numeral_items  # pyright: ignore[reportPrivateUsage]

    def test_greek_aegean_items_match_map(self) -> None:
        """Aegean: 45-entry map, Unicode multi-char glyphs."""
        m = systems.greek.Aegean._to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert tuple(m.items()) == systems.greek.Aegean._to_numeral_items  # pyright: ignore[reportPrivateUsage]

    def test_attic_int_items_match_map(self) -> None:
        """Attic: the integer-only subset map used in the hot path."""
        m = systems.greek.Attic._int_to_numeral_map  # pyright: ignore[reportPrivateUsage]
        assert tuple(m.items()) == systems.greek.Attic._int_to_numeral_items  # pyright: ignore[reportPrivateUsage]


class TestIsValidDenotation:
    """Regression tests for System.is_valid_denotation() type-check fast path.

    The fast path uses ``type(val) in frozenset`` which bypasses isinstance MRO
    traversal for the common case.  These tests confirm that the bool/subclass
    fallback and the wrong-type rejection still behave correctly.
    """

    def test_plain_int_accepted(self) -> None:
        """Plain int is the common denotation type — must return True."""
        assert systems.hindu_arabic.Arabic.is_valid_denotation(42)

    def test_bool_as_int_not_accepted(self) -> None:
        """bool is a subclass of int; must return True despite type(True) != int."""
        assert not systems.hindu_arabic.Arabic.is_valid_denotation(True)

    def test_fraction_accepted_for_roman_standard(self) -> None:
        """roman.Standard accepts int | Fraction denotations."""
        assert systems.roman.Standard.is_valid_denotation(Fraction(1, 2))

    def test_str_rejected_for_int_system(self) -> None:
        """str is not a valid denotation for Arabic."""
        assert not systems.hindu_arabic.Arabic.is_valid_denotation("42")

    def test_fraction_rejected_for_int_only_system(self) -> None:
        """Fraction is not valid for systems that only accept int."""
        assert not systems.mayan.Mayan.is_valid_denotation(Fraction(1, 2))
