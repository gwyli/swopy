"""
Tests for specific cases

This module is for non-property-based system specific tests. Each system should
have its own class for organisation in the form Test<Module><Class>
"""

# Ignore ambiguous unicode character strings in Roman numerals (e.g., 'I' vs 'Ⅰ').
# ruff: noqa: RUF002 RUF003

from collections.abc import Mapping
from fractions import Fraction

import pytest
from hypothesis import given, strategies

from swopy import systems
from swopy.systems._algorithms import (
    greedy_additive_to_numeral,
    reversed_greedy_additive_to_numeral,
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


class TestAlgorithmsGreedyAdditive:
    """Checks that any new greedy_additive_to_numeral matches the verbatim original.

    The reference implementation below is a permanent copy of the algorithm as it
    existed before any optimisation.  These tests should remain unchanged so that
    future rewrites can be validated against it.
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
        assert greedy_additive_to_numeral(number, m) == self._reference(number, m)

    @given(strategies.integers(min_value=1, max_value=999))
    def test_nabataean(self, number: int) -> None:
        """Nabataean map: non-power-of-10 denominations — exercises sparse glyphs."""
        m = systems.nabataean.Nabataean.to_numeral_map()
        assert greedy_additive_to_numeral(number, m) == self._reference(number, m)

    @given(strategies.integers(min_value=1, max_value=9999))
    def test_reversed_pahlavi(self, number: int) -> None:
        """InscriptionalParthian — exercises the reversed (RTL) variant."""
        m = systems.pahlavi.InscriptionalParthian.to_numeral_map()
        assert (
            reversed_greedy_additive_to_numeral(number, m)
            == self._reference(number, m)[::-1]
        )
