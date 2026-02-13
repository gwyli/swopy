"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between Arabic numerals and
their representations in that particular numeral system.
"""

from abc import ABC, abstractmethod
from fractions import Fraction
from sys import float_info
from types import UnionType, get_original_bases
from typing import Any, ClassVar, TypeIs, cast, get_args

type Numeral = int | float | Fraction | str
type Denotation = int | Fraction | float


class System[TNumeral: (Numeral), TDenotation: (Denotation)](ABC):
    """Abstract base class for numeral system converters.

    Defines the interface that all numeral system implementations must follow,
    including conversion methods and range constraints. Subclasses implement
    specific numeral systems (Roman, Egyptian, Arabic, etc.) with their
    own conversion logic and valid ranges.

    Type Parameters:
        Numeral: The representation type of the numeral system.

    Attributes:
        to_numeral_map: Mapping from Arabic numbers to their representations in the
            numeral system.
        from_numeral_map: Mapping from the representation in the numeral system to
            Arabic numbers.
        minimum: The minimum valid value for this numeral system.
        maximum: The maximum valid value for this numeral system.
        maximum_is_many: Whether the maximum is precise or represents "many".
    """

    to_numeral_map: ClassVar[dict[int, str]]
    from_numeral_map: ClassVar[dict[str, int]]

    minimum: ClassVar[float] = -float_info.max
    maximum: ClassVar[float] = float_info.max
    maximum_is_many: ClassVar[bool] = False
    _numeral_runtime_type: ClassVar[tuple[type, ...]]
    _denotation_runtime_type: ClassVar[tuple[type, ...]]

    def __init_subclass__(cls, **kwargs: dict[Any, Any]) -> None:
        """Appends the base types of the numeral system to the class variable for
        runtime type checking.
        """
        super().__init_subclass__(**kwargs)

        cls._numeral_runtime_type = cls._get_base_types(0)
        cls._denotation_runtime_type = cls._get_base_types(1)

    @classmethod
    def _get_base_types(cls, position: int) -> tuple[type]:
        """Returns the base type of the numeral system. When multiple types are
        supported, unfurl the UnionType and return all base types.

        Returns:
            The base type(s) used for numeral representation in this system.
        """

        base: type | UnionType = get_original_bases(cls)[0]

        denotation: type | UnionType = get_args(base)[position]

        if isinstance(denotation, UnionType):
            return get_args(denotation)

        return (denotation,)

    @classmethod
    def is_valid_numeral(cls, val: Any) -> TypeIs[TNumeral]:
        """Checks if a numeral has a valid type for this numeral system."""
        return isinstance(val, cls._numeral_runtime_type)

    @classmethod
    def is_valid_denotation(cls, val: Any) -> TypeIs[TDenotation]:
        """Checks if a denotation has a valid type for this numeral system."""
        return isinstance(val, cls._denotation_runtime_type)

    @classmethod
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

        number_: Denotation = number

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
        """Converts an Arabic number to the numeral system's representation.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.
        """
        ...

    @classmethod
    @abstractmethod
    def from_numeral(cls, numeral: TNumeral) -> TDenotation:
        """Converts a numeral representation to an Arabic number.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.
        """
        ...
