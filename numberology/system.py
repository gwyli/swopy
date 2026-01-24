"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between integer values and
their string/integer representations in that particular numeral system.
"""

from abc import ABC, abstractmethod
from sys import maxsize
from typing import ClassVar

Numeral = str | int


class System[Numeral](ABC):
    """Abstract base class for numeral system converters.

    Defines the interface that all numeral system implementations must follow,
    including conversion methods and range constraints. Subclasses implement
    specific numeral systems (Roman, Egyptian, Arabic, Latin, etc.) with their
    own conversion logic and valid ranges.

    Type Parameters:
        Numeral: The representation type of the numeral system (str or int).

    Attributes:
        from_int_: Mapping from integers to their numeral representation strings.
        to_int_: Mapping from numeral strings to their integer values.
        minimum: The minimum valid value for this numeral system.
        maximum: The maximum valid value for this numeral system.
        maximum_is_many: Whether the maximum is precise or represents "many".
    """

    from_int_: ClassVar[dict[int, str]]
    to_int_: ClassVar[dict[str, int]]

    minimum: ClassVar[int] = -maxsize
    maximum: ClassVar[int] = maxsize
    maximum_is_many: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def _limits(cls, number: int) -> int:
        """Validates that a number is within acceptable limits for the system.

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Raises:
            ValueError: If the number is outside the valid range.
        """
        ...

    @classmethod
    @abstractmethod
    def from_int(cls, number: int) -> str | int:
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
    def to_int(cls, number: Numeral) -> int:
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
