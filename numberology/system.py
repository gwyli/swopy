"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between integer values and
their string/integer representations in that particular numeral system.
"""

from abc import ABC, abstractmethod
from fractions import Fraction
from sys import float_info
from typing import ClassVar, cast

type Numeral = int | float | Fraction | str
type Denotation = int | Fraction | float


class System[TNumeral: (Numeral), TDenotation: (Denotation)](ABC):
    """Abstract base class for numeral system converters.

    Defines the interface that all numeral system implementations must follow,
    including conversion methods and range constraints. Subclasses implement
    specific numeral systems (Roman, Egyptian, Arabic, Latin, etc.) with their
    own conversion logic and valid ranges.

    Type Parameters:
        Numeral: The representation type of the numeral system (str or int).

    Attributes:
        to_numeral_map: Mapping from integers to their numeral representation strings.
        from_numeral_map: Mapping from numeral strings to their integer values.
        minimum: The minimum valid value for this numeral system.
        maximum: The maximum valid value for this numeral system.
        maximum_is_many: Whether the maximum is precise or represents "many".
    """

    to_numeral_map: ClassVar[dict[int, str]]
    from_numeral_map: ClassVar[dict[str, int]]

    minimum: ClassVar[float] = -float_info.max
    maximum: ClassVar[float] = float_info.max
    maximum_is_many: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def _limits(cls, number: TDenotation) -> TDenotation:
        """Validates that a number is within acceptable limits for the system.

        Args:
            number: The number to validate.

        Returns:
            The validated number, replacing the number with maximum if the numeral
                system uses "many" for values at or above the maximum.

        Raises:
            ValueError: If the number is outside the valid range.
        """

        number_: float | Fraction | int = number

        if number_ < cls.minimum:
            raise ValueError(f"Number must be greater or equal to {cls.minimum}.")

        if cls.maximum_is_many:
            number_ = min(number_, cls.maximum)

        if number_ > cls.maximum:
            raise ValueError(f"Number must be less than or equal to {cls.maximum}.")

        # and back again to the expected type
        return cast(TDenotation, number_)

    @classmethod
    @abstractmethod
    def to_numeral(cls, number: TDenotation) -> TNumeral:
        """Converts an integer to the numeral system's representation.

        Args:
            number: The integer to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.
        """
        ...

    @classmethod
    @abstractmethod
    def from_numeral(cls, number: TNumeral) -> TDenotation:
        """Converts a numeral representation to an integer.

        Args:
            number: The numeral to convert (string or int depending on system).

        Returns:
            The integer value of the numeral.

        Raises:
            ValueError: If the number is outside the valid range.
            ValueError: If the numeral representation is invalid.
        """
        ...
