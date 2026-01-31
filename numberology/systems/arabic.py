"""Arabic numeral system conversion module.

This module provides conversion utilities for Arabic numerals (1, 2, 3, ...).
It's a placeholder module since Arabic numerals are the standard integer representation.
"""

from numberology.system import RealNumber, System


class Arabic(System[RealNumber]):
    """Arabic numeral system converter.

    Implements conversion for Arabic numerals (0-9), the standard modern numeral
    system used worldwide. Since Arabic numerals are the native integer representation
    in Python, this implementation serves as a pass-through converter.

    Type Parameter:
        int: Arabic numerals are represented as integers.

    Attributes:
        from_int_: Not used; integers are returned as-is.
        to_int_: Not used; integers are validated and returned as-is.
        minimum: Minimum representable value (-sys.float_info.max).
        maximum: Maximum representable value (sys.float_info.max).
        maximum_is_many: False, as the maximum is a precise limit.
    """

    @classmethod
    def _input_type_guard(cls, number: RealNumber) -> RealNumber:
        """Checks if the provided number matches the numeral system's base type.

        Args:
            number: The number to check.
        """
        if not isinstance(number, RealNumber):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("Number must be of type RealNumber.")

        return number

    @classmethod
    def from_int(cls, number: RealNumber) -> RealNumber:
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
    def to_int(cls, number: RealNumber) -> RealNumber:
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
        return cls._limits(number)
