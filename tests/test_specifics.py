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
    char_sum_from_numeral,
    greedy_additive_to_numeral,
    longest_match_from_numeral,
    multiplicative_additive_from_numeral,
    multiplicative_myriad_from_numeral,
    positional_to_numeral,
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
