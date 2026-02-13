"""Arabic numeral system conversion module.

This module provides conversion utilities for Arabic numerals (1, 2, 3, ...).
Since Arabic numerals are the native numeral representation in Python, this
implementation serves as a pass-through converter.
"""

from fractions import Fraction

from swopy.system import System


class Arabic[TNumeral: float | Fraction | int, TDenotation: float | Fraction | int](
    System[float | Fraction | int, float | Fraction | int]
):
    """Arabic numeral system converter.

    Implements conversion for Arabic numerals (0-9), the standard modern numeral
    system used worldwide. Since Arabic numerals are the native numeral representation
    in Python, this implementation serves as a pass-through converter.

    Attributes:
        to_numeral_map: Not used; integers are returned as-is.
        from_numeral_map: Not used; numbers are validated and returned as-is.
        minimum: Minimum representable value (-sys.float_info.max).
        maximum: Maximum representable value (sys.float_info.max).
        maximum_is_many: False, as the maximum is a precise limit.
    """

    @classmethod
    def to_numeral(cls, number: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting a number to a Arabic numeral.

        Args:
            number: The number to convert.

        Returns:
            The input as Arabic numerals are the standard numeral representation in
            Python.

        Examples:
            >>> Arabic.to_numeral(1)
            1
            >>> Arabic.to_numeral(42)
            42
        """
        return cls._limits(number)

    @classmethod
    def from_numeral(cls, number: float | Fraction | int) -> float | Fraction | int:
        """Placeholder function for converting an Arabic numeral to an number.

        Args:
            number: The Arabic numeral to convert.
        Returns:
            The input as Arabic numerals are the standard numeral representation in
            Python.

        Examples:
            >>> Arabic.from_numeral(1)
            1
            >>> Arabic.from_numeral(42)
            42
        """
        return cls._limits(number)
