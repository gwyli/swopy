"""Egyptian numeral system conversion module.

This module provides conversion utilities for Egyptian hieroglyphic numerals.
It implements bidirectional conversion between Arabic numbers and Egyptian numerals.
"""

from typing import ClassVar, Literal

from swopy.system import System


class Egyptian(System[str, int]):
    """Egyptian hieroglyphic numeral system converter.

    Implements bidirectional conversion between integers and Egyptian hieroglyphic
    numerals. Uses a base-10 system with individual hieroglyph symbols for powers of 10
    (1, 10, 100, 1000, 10000, 100000, 1000000). Numbers above 999,999 are
    considered "many" and capped at the maximum of 1,000,000.

    Attributes:
        to_numeral_map: Mapping of powers of 10 to their corresponding hieroglyph.
        from_numeral_map: Reverse mapping of hieroglyphs to their integer values.
        minimum: Minimum valid value (1).
        maximum: Maximum representable value (1,000,000).
        maximum_is_many: True, indicating the maximum represents "many" in Egyptian
            notation.
    """

    to_numeral_map: ClassVar[dict[int, str]] = {
        1_000_000: "\U00013069",
        100_000: "\U00013153",
        10_000: "\U000130ad",
        1_000: "\U000131bc",
        100: "\U00013362",
        10: "\U00013386",
        1: "\U000133fa",
    }

    from_numeral_map: ClassVar[dict[str, int]] = {
        v: k for k, v in to_numeral_map.items()
    }

    minimum: ClassVar[float] = 1
    maximum: ClassVar[float] = 1_000_000

    maximum_is_many: ClassVar[bool] = True
    encodings: ClassVar[set[Literal["utf8", "ascii"]]] = {"utf8"}

    @classmethod
    def _to_numeral(cls, number: int) -> str:
        """Converts an integer to an Egyptian numeral.

        Takes an integer and converts it to its Egyptian hieroglyph representation
        using the base-10 system of hieroglyphic symbols.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Egyptian.to_numeral(1)
            '\U000133fa'
            >>> Egyptian.to_numeral(101)
            '\U00013362\U000133fa'
            >>> Egyptian.to_numeral(1000001)
            '\U00013069'
        """
        result: str = ""

        for arabic, hieroglyph in cls.to_numeral_map.items():
            count, number = divmod(number, arabic)
            count = int(count)
            result += hieroglyph * count

        return result

    @classmethod
    def _from_numeral(cls, numeral: str) -> int:
        """Converts an Egyptian numeral to an integer.

        Takes an Egyptian numeral and converts it to its integer equivalent
        by summing the values of each hieroglyph.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.

        Examples:
            >>> Egyptian.from_numeral("\U000133fa")  # Single unit hieroglyph
            1
            >>> Egyptian.from_numeral("\U00013386")  # Ten hieroglyph
            10
        """
        total: int = 0

        for hieroglyph in numeral:
            if hieroglyph not in cls.from_numeral_map:
                raise ValueError(f"Invalid Egyptian hieroglyph: {hieroglyph}")
            total += cls.from_numeral_map[hieroglyph]

        return total
