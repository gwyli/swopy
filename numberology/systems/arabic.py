"""Arabic numeral system conversion module.

This module provides conversion utilities for Arabic numerals (1, 2, 3, ...).
It's a placeholder module since Arabic numerals are the standard integer representation.
"""

from numberology.system import System


class Arabic(System[int]):
    @classmethod
    def _limits(cls, number: int) -> int:
        """Placeholder function for validating Arabic numerals.

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Examples:
            >>> Arabic._limits(10)
            10
            >>> Arabic._limits(3999)
            3999
        """
        return number

    @classmethod
    def from_int(cls, number: int) -> int:
        """Placeholder function for converting an integer to a Arabic numeral.

        Args:
            number: The integer to convert.

        Returns:
            The Arabic numeral representation of the number.

        Examples:
            >>> Arabic.from_int(1)
            1
            >>> Arabic.from_int(42)
            42
        """
        return cls._limits(number)

    @classmethod
    def to_int(cls, number: int | str) -> int:
        """Placeholder function for converting an Arabic numeral to an integer.

        Args:
            number: The Arabic numeral to convert.
        Returns:
            The integer representation of the Arabic numeral.

        Examples:
            >>> Arabic.to_int(1)
            1
            >>> Arabic.to_int(42)
            42
        """
        return cls._limits(int(number))
