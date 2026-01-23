"""Egyptian numeral system conversion module.

This module provides conversion utilities for Egyptian hieroglyphic numerals.
Egyptian numerals use a base-10 system with unique hieroglyph symbols for
values 1, 10, 100, 1000, 10000, 100000, and 1000000.
"""

from typing import ClassVar

from numberology.system import System


class Egyptian(System[str]):
    from_int_: ClassVar[dict[int, str]] = {
        1_000_000: "\U00013069",
        100_000: "\U00013153",
        10_000: "\U000130ad",
        1_000: "\U000131bc",
        100: "\U00013362",
        10: "\U00013386",
        1: "\U000133fa",
    }

    to_int_: ClassVar[dict[str, int]] = {v: k for k, v in from_int_.items()}

    minimum: ClassVar[int] = 1
    maximum: ClassVar[int] = 1_000_000

    maximum_is_many: ClassVar[bool] = True

    @classmethod
    def _limits(cls, number: int) -> int:
        """Validates that a number is within acceptable limits for Egyptian numerals.

        As the Egyptian numeral system typically represents numbers over 999,999 as
        "many", this method ensures the number is at least 1 and caps it at 1,000,000.

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Egyptian._limits(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be greater than 0.
            >>> Egyptian._limits(1)
            1
            >>> Egyptian._limits(1000001)
            1000000
        """
        if number < cls.minimum:
            raise ValueError(f"Number must be greater than {cls.minimum}.")

        number_: int = min(number, cls.maximum)

        return number_

    @classmethod
    def from_int(cls, number: int) -> str:
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
            >>> Egyptian.from_int(1) == "\U000133fa"
            True
            >>> Egyptian.from_int(101) == "\U00013362\U000133fa"
            True
        """
        result = ""
        number_ = cls._limits(number)

        for latin, hieroglyph in cls.from_int_.items():
            count, number_ = divmod(number_, latin)
            result += hieroglyph * count

        return result

    @classmethod
    def to_int(cls, number: str) -> int:
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
            >>> Egyptian.to_int("\U000133fa")  # Single unit hieroglyph
            1
            >>> Egyptian.to_int("\U00013386")  # Ten hieroglyph
            10
        """
        total: int = 0
        for hieroglyph in number:
            if hieroglyph not in cls.to_int_:
                raise ValueError(f"Invalid Egyptian hieroglyph: {hieroglyph}")
            total += cls.to_int_[hieroglyph]

        return cls._limits(total)
