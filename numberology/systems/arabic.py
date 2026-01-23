"""Arabic numeral system conversion module.

This module provides conversion utilities for Arabic numerals (1, 2, 3, ...).
It's a placeholder module since Arabic numerals are the standard integer representation.
"""

from sys import maxsize
from typing import ClassVar

from numberology.system import System


class Arabic(System[int]):
    minimum: ClassVar[int] = -maxsize
    maximum: ClassVar[int] = maxsize

    maximum_is_many: ClassVar[bool] = False

    @staticmethod
    def _limits(number: int) -> int:
        """Placeholder function for validating Arabic numerals.

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Arabic._limits(10)
            10
            >>> Arabic._limits(3999)
            3999
        """
        return number

    @staticmethod
    def from_int(number: int) -> int:
        """Placeholder function for converting an integer to a Arabic numeral.

        Args:
            number: The integer to convert.

        Returns:
            The Arabic numeral representation of the number.

        Examples:
            >>> Arabic.from_int(1)
            1
            >>> Arabic.from_int(10)
            10
            >>> Arabic.from_int(42)
            42
        """
        return Arabic._limits(number)

    @staticmethod
    def to_int(number: int | str) -> int:
        """Placeholder function for converting an Arabic numeral to an integer.

        Args:
            number: The Arabic numeral to convert.

        Returns:
            The integer representation of the Arabic numeral.

        Examples:
            >>> Arabic.to_int(1)
            1
            >>> Arabic.to_int(10)
            10
            >>> Arabic.to_int(42)
            42
        """
        return Arabic._limits(int(number))
