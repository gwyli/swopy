"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between integer values and
their string/integer representations in that particular numeral system.
"""

from abc import ABC, abstractmethod
from fractions import Fraction
from sys import float_info
from types import NoneType, UnionType, get_original_bases
from typing import ClassVar, TypeVar, get_args

RealNumber = float | int | Fraction
# TypeVar to maintain the relationship between numeral representation and system type.
TNumeral = TypeVar("TNumeral", RealNumber, Fraction | int, int, str)


class System[TNumeral](ABC):
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

    minimum: ClassVar[RealNumber] = -float_info.max
    maximum: ClassVar[RealNumber] = float_info.max
    maximum_is_many: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def _base_types(cls, obj: type | None = None) -> set[type | UnionType]:
        """Returns the base type of the numeral system. When multiple types are
        supported, unfurl the UnionType and return all base types.

        Returns:
            The base type(s) used for numeral representation in this system.
        """
        type_ = obj or cls
        original_base: type = get_original_bases(type_)[0]
        types: tuple[type | NoneType | UnionType] = get_args(original_base)

        # Occurs if the class is subclassed without specifying a type parameter.
        # Walk back to the original base to get the correct type parameter.
        if types == ():
            return cls._base_types(obj=original_base)

        if isinstance(types[0], NoneType):
            raise ValueError("Numeral system base type cannot be NoneType.")

        return {types[0]}

    @classmethod
    @abstractmethod
    def _dict_types(cls) -> set[type]:
        """Returns the set of types used in to_numeral_map and from_numeral_map
        dictionaries.

        Returns:
            The set of types used for numeral representation in this system.
        """
        return {type(x) for x in cls.to_numeral_map} | {
            type(x) for x in cls.from_numeral_map.values()
        }

    @classmethod
    @abstractmethod
    def _input_type_guard(cls, number: RealNumber) -> RealNumber:
        """Checks if the provided number matches the numeral system's base type.

        Args:
            number: The number to check.
        """
        types: set[type]

        if RealNumber in cls._base_types():
            types = set(get_args(RealNumber))
        else:
            types = cls._dict_types()

        if type(number) not in types:
            raise ValueError(
                f"Number must be of type {', '.join(x.__name__ for x in types)}."
            )

        return number

    @classmethod
    @abstractmethod
    def _limits(cls, number: RealNumber) -> RealNumber:
        """Validates that a number is within acceptable limits for the system.

        Args:
            number: The number to validate.

        Returns:
            The validated number, replacing the number with maximum if the numeral
                system uses "many" for values at or above the maximum.

        Raises:
            ValueError: If the number is outside the valid range.
        """

        number_: RealNumber = cls._input_type_guard(number)

        if number_ < cls.minimum:
            raise ValueError(f"Number must be greater or equal to {cls.minimum}.")

        if cls.maximum_is_many:
            number_ = min(number, cls.maximum)

        if number_ > cls.maximum:
            raise ValueError(f"Number must be less than or equal to {cls.maximum}.")

        return number_

    @classmethod
    @abstractmethod
    def to_numeral(cls, number: RealNumber) -> TNumeral:
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
    def from_numeral(cls, number: TNumeral) -> int | RealNumber:
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
