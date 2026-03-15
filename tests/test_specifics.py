"""
Tests for specific cases

This module is for non-property-based system specific tests. Each system should
have its own class for organisation in the form Test<Module><Class>
"""

# Ignore ambiguous unicode character strings in Roman numerals (e.g., 'I' vs 'Ⅰ').
# ruff: noqa: RUF003

from fractions import Fraction

import pytest

from swopy import systems


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


class TestEtruscanEtruscan:
    """Specific tests for systems.etruscan.Etruscan."""

    def test_to_numeral_four(self):
        # 4 = 4×1; Etruscan has no subtractive notation
        assert systems.etruscan.Etruscan.to_numeral(4) == "\U00010320" * 4

    def test_to_numeral_six(self):
        # 6 = 1 + 5; RTL → smallest on the left: 𐌠𐌡
        assert systems.etruscan.Etruscan.to_numeral(6) == "\U00010320" + "\U00010321"

    def test_to_numeral_seventeen(self):
        # 17 = 2×1 + 1×5 + 1×10; RTL: 𐌠𐌠𐌡𐌢
        assert (
            systems.etruscan.Etruscan.to_numeral(17)
            == "\U00010320" * 2 + "\U00010321" + "\U00010322"
        )

    def test_to_numeral_twentynine(self):
        # 29 = 4×1 + 1×5 + 2×10; RTL: 𐌠𐌠𐌠𐌠𐌡𐌢𐌢
        assert (
            systems.etruscan.Etruscan.to_numeral(29)
            == "\U00010320" * 4 + "\U00010321" + "\U00010322" * 2
        )


class TestIndicKharosthi:
    """Specific tests for systems.indic.Kharosthi"""

    def test_to_numeral(self):
        # 2+4+10+20+20+20+20 + 100x(1+4+4) + 1000
        assert systems.indic.Kharosthi.to_numeral(1996) == "𐩇𐩃𐩃𐩀𐩆𐩅𐩅𐩅𐩅𐩄𐩃𐩁"


class TestGreekAttic:
    """Specific tests for systems.greek.Attic."""

    def test_non_representable_fraction(self) -> None:
        """Checks that a ValueError is raised for a fraction that cannot be
        represented in Attic numerals (only 1/2 and 1/4 are supported).
        """
        with pytest.raises(ValueError):
            systems.greek.Attic.to_numeral(Fraction(1, 3))


class TestAramaicImperialAramaic:
    """Specific tests for systems.aramaic.ImperialAramaic."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.aramaic.ImperialAramaic.to_numeral(1001)
        assert numeral[-1] == "\U0001085e"  # ONE THOUSAND on right


class TestAramaicManichaean:
    """Specific tests for systems.aramaic.Manichaean."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.aramaic.Manichaean.to_numeral(11)
        assert numeral[-1] == "\U00010aed"  # TEN on right


class TestAramaicOldSogdian:
    """Specific tests for systems.aramaic.OldSogdian."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.aramaic.OldSogdian.to_numeral(101)
        assert numeral[-1] == "\U00010f25"  # ONE HUNDRED on right


class TestAramaicSogdian:
    """Specific tests for systems.aramaic.Sogdian."""

    def test_rtl(self) -> None:
        """Checks that larger denominations appear on the right (RTL order)."""
        numeral = systems.aramaic.Sogdian.to_numeral(21)
        assert numeral[-1] == "\U00010f53"  # TWENTY on right


class TestAncientSouthArabian:
    """Specific tests for systems.semetic.OldSouthArabian"""

    def test_to_numeral(self):
        assert systems.semetic.AncientSouthArabian.to_numeral(31000) == "𐩲𐩲𐩲𐩱"
        assert systems.semetic.AncientSouthArabian.to_numeral(40000) == "𐩲𐩲𐩲𐩲"
