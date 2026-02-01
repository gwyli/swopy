"""Egyptian numeral system conversion module.

This module provides conversion utilities for Egyptian hieroglyphic numerals.
Egyptian numerals use a base-10 system with unique hieroglyph symbols for
values 1, 10, 100, 1000, 10000, 100000, and 1000000.
"""

from typing import ClassVar

from numberology.system import RealNumber, System


class Egyptian(System[str]):
    """Egyptian hieroglyphic numeral system converter.

    Implements bidirectional conversion between integers and Egyptian hieroglyphic
    numerals. Uses a base-10 system with individual hieroglyph symbols for powers of 10
    (1, 10, 100, 1000, 10000, 100000, 1000000). Numbers above 999,999 are
    considered "many" and capped at the maximum of 1,000,000.

    Type Parameter:
        str: Egyptian numerals are represented as strings of Unicode hieroglyph
            characters.

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

    minimum: ClassVar[RealNumber] = 1
    maximum: ClassVar[RealNumber] = 1_000_000

    maximum_is_many: ClassVar[bool] = True

    @classmethod
    def to_numeral(cls, number: RealNumber) -> str:
        """Converts an integer to an Egyptian numeral.

        Takes an integer and converts it to its Egyptian hieroglyph representation
        using the base-10 system of hieroglyphic symbols.

        Args:
            number: The integer to convert.

        Returns:
            The hieroglyphic representation of the number.

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
        number_: RealNumber = cls._limits(number)

        for arabic, hieroglyph in cls.to_numeral_map.items():
            count, number_ = divmod(number_, arabic)
            count = int(count)
            result += hieroglyph * count

        return result

    @classmethod
    def from_numeral(cls, number: str) -> RealNumber:
        """Converts an Egyptian numeral to an integer.

        Takes an Egyptian numeral and converts it to its integer equivalent
        by summing the values of each hieroglyph.

        Args:
            number: The Egyptian numeral to convert.

        Returns:
            The integer representation of the Egyptian numeral.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Egyptian.from_numeral("\U000133fa")  # Single unit hieroglyph
            1
            >>> Egyptian.from_numeral("\U00013386")  # Ten hieroglyph
            10
        """
        total: int = 0
        for hieroglyph in number:
            if hieroglyph not in cls.from_numeral_map:
                raise ValueError(f"Invalid Egyptian hieroglyph: {hieroglyph}")
            total += cls.from_numeral_map[hieroglyph]

        return cls._limits(total)
