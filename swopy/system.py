"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between Arabic numerals and
their representations in that particular numeral system.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from fractions import Fraction
from math import inf
from types import UnionType, get_original_bases
from typing import Any, ClassVar, Literal, TypeIs, get_args

from .systems._translations import ASCII

type Numeral = int | float | Fraction | str
type Denotation = int | Fraction | float
type Encodings = set[Literal["utf8", "ascii"]]


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

    minimum: ClassVar[int | float | Fraction] = -inf
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    _to_numeral_map: Mapping[TDenotation, TNumeral]
    _from_numeral_map: Mapping[TNumeral, TDenotation]

    _numeral_runtime_type: ClassVar[tuple[type, ...]]
    _denotation_runtime_type: ClassVar[tuple[type, ...]]
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Appends the base types of the numeral system to the class variable for
        runtime type checking.
        """
        super().__init_subclass__(**kwargs)

        cls._numeral_runtime_type = cls._get_base_types(0)
        cls._denotation_runtime_type = cls._get_base_types(1)

    @classmethod
    def to_numeral_map(cls) -> Mapping[TDenotation, TNumeral]:
        """Returns the map for converting from Arabic numbers to this systems numerals.

        This method exists as a typed accessor for the ``_map`` class variable rather
        than exposing ``_map`` directly. PEP 526 prohibits ``ClassVar`` from containing
        type variables, and PEP 484's invariance rule for mutable bindings means a
        subclass cannot narrow ``Mapping[str, object]`` to ``Mapping[str, int]`` without
        a type error. Returning ``TDenotation`` from a classmethod is valid because
        PEP 695 type parameters on a generic class are resolved through the instance-
        typed generic machinery introduced in PEP 484.

        Returns:
            A mapping from Arabic numerals to their denotation in this system.
        """
        return cls._to_numeral_map

    @classmethod
    def from_numeral_map(cls) -> Mapping[TNumeral, TDenotation]:
        """Returns the map for converting to Arabic numbers from this systems numerals.

        Additional rationale detailed in ``to_numeral_map()``

        Returns:
            A mapping from the numberal systems denotation to Arabic numerals
        """
        return cls._from_numeral_map

    @classmethod
    def _get_base_types(cls, position: int) -> tuple[type, ...]:
        """Returns the base type of the numeral system. When multiple types are
        supported, unfurl the UnionType and return all base types.

        Returns:# Code review agent
            The base type(s) used for numeral representation in this system.
        """

        base: type[System[TNumeral, TDenotation]] = get_original_bases(cls)[0]

        types: tuple[type | UnionType] = get_args(base)

        if types == ():
            types = get_args(get_original_bases(base)[0])

        types_: type | UnionType = types[position]

        if isinstance(types_, UnionType):
            return get_args(types_)

        return (types_,)

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

        number_: TDenotation = number
        # Avoiding class instance lookups saves an average of 5% of execution time
        minimum = cls.minimum
        maximum = cls.maximum

        if number_ < minimum:
            raise ValueError(f"Number must be greater or equal to {minimum}.")

        if cls.maximum_is_many and number_ > maximum:
            # cls.maximum is a float, which is not assignable to number_
            # Ignore the type checker to remove an average of two cast() calls per call
            # to swopy.swop(), which was taking 4.6-12.5% of execution time.
            return maximum  # pyright: ignore[reportReturnType]

        if number_ > maximum:
            raise ValueError(f"Number must be less than or equal to {maximum}.")

        # and back again to the expected type
        return number_

    @classmethod
    @abstractmethod
    def _to_numeral(cls, number: TDenotation) -> TNumeral:
        """Internal method to convert an Arabic number to the numeral system's
        representation.

        This method is intended to be implemented by subclasses with the actual
        conversion logic, while the public `to_numeral` method handles validation
        and type checking.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.
        """
        ...

    @classmethod
    def to_numeral(
        cls,
        number: TDenotation,
        encode: Literal["utf8", "ascii"] = "utf8",
    ) -> TNumeral:
        """Converts an Arabic number to the numeral system's representation.

        Where applicable, to_numeral() returns a UTF-8 string representation of the
        numeral by default. The 'ascii', encoding can be used to return a pure ASCII
        representation instead.

        Args:
            number: The Arabic number to convert.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range.
        """

        if not cls.is_valid_denotation(number):
            raise TypeError(
                f"{number} of type {type(number).__name__} cannot be represented in {cls.__name__}."  # noqa: E501
            )

        return cls.to_numeral_trusted(number, encode=encode)

    @classmethod
    def to_numeral_trusted(
        cls,
        number: TDenotation,
        encode: Literal["utf8", "ascii"] = "utf8",
    ) -> TNumeral:
        """Like to_numeral() but omits the is_valid_denotation guard.

        Called from swop() after TypeIs narrowing has already confirmed the
        denotation type. Do not call directly unless type is already validated.

        Args:
            number: The Arabic number to convert (type already validated by caller).
            encode: The encoding to use for the output string.

        Returns:
            The representation of the number in this numeral system.

        Raises:
            ValueError: If the number is outside the valid range or encoding is
                unsupported.
        """
        if encode not in cls.encodings:
            raise ValueError(
                f"Encoding '{encode}' is not supported for {cls.__name__}."
            )

        number_: TDenotation = cls._limits(number)

        numeral: TNumeral = cls._to_numeral(number_)

        if encode == "ascii" and isinstance(numeral, str):
            # numeral.translate is a str, which is a subset of TNumeral
            # Ignore the type checker to remove an average of two cast() calls per call
            # to swopy.swop(), which was taking 4.6-12.5% of execution time.
            return numeral.translate(ASCII)  # pyright: ignore[reportReturnType]

        return numeral

    @classmethod
    @abstractmethod
    def _from_numeral(cls, numeral: TNumeral) -> TDenotation:
        """Converts a numeral representation to an Arabic number.

        This method is intended to be implemented by subclasses with the actual
        conversion logic, while the public `from_numeral` method handles validation
        and type checking.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.
        """

    @classmethod
    def from_numeral(
        cls,
        numeral: TNumeral,
    ) -> TDenotation:
        """Converts a numeral representation to an Arabic number.

        Accepts both UTF-8 and Latin-character forms of numerals unconditionally;
        system maps include entries for both representations.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral in Arabic numerals.

        Raises:
            ValueError: If the Arabic representation of the numeral is outside the valid
                range.
            ValueError: If the numeral representation is invalid.
        """
        if not cls.is_valid_numeral(numeral):
            raise TypeError(  # pyright: ignore[reportUnreachable]
                f"{numeral} of type {type(numeral).__name__} cannot be represented in {cls.__name__}."  # noqa: E501
            )

        number: TDenotation = cls._from_numeral(numeral)

        return cls._limits(number)
