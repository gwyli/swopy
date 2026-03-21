"""Abstract base class for numeral system converters.

This module defines the System abstract base class that serves as the foundation
for implementing different numeral systems (e.g., Roman, Egyptian, Arabic). Each
concrete system implementation defines how to convert between Western Arabic numerals
and that particular numeral system.
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
    specific numeral systems (Egyptian, Arabic, Mayan etc.) with their
    own conversion logic and valid ranges.

    Type Parameters:
        TNumeral: The numeral being denoted
        TDenotation: The denotation of the numeral in the system

    Attributes:
        minimum: The minimum valid denotation for this numeral system
        maximum: The maximum valid denotation for this numeral system
        maximum_is_many: Whether the maximum is precise or represents "many"
        encodings: The encodings the numeral system supports
    """

    minimum: ClassVar[int | float | Fraction] = -inf
    maximum: ClassVar[int | float | Fraction] = inf
    maximum_is_many: ClassVar[bool] = False
    encodings: ClassVar[Encodings] = {"utf8", "ascii"}

    # Mapping from denotation to the numeral representations in the system
    _to_numeral_map: Mapping[TDenotation, TNumeral]

    # Mapping from the numeral representation in the system to their denotation
    _from_numeral_map: Mapping[TNumeral, TDenotation]

    # The subtypes of Numeral supported by the system
    _numeral_runtime_type: ClassVar[frozenset[type]]

    # The subtypes of Denotation supported by the system
    _denotation_runtime_type: ClassVar[frozenset[type]]

    # Does the class have bounds, or does it extend from -inf to inf?
    _bounded: ClassVar[bool] = True

    # Conversion of ``_to_numeral_map`` to a tuple for quicker access in
    # ``systems._algorithms``
    _to_numeral_items: ClassVar[tuple[tuple[Any, Any], ...]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Precalculates private class variables for later use. Descriptions of each
        are provided in the class declaration.
        """
        super().__init_subclass__(**kwargs)

        cls._numeral_runtime_type = frozenset(cls._get_base_types(0))
        cls._denotation_runtime_type = frozenset(cls._get_base_types(1))
        cls._bounded = not (cls.minimum == -inf and cls.maximum == inf)

        if hasattr(cls, "_to_numeral_map"):
            cls._to_numeral_items = tuple(cls._to_numeral_map.items())

    @classmethod
    def to_numeral_map(cls) -> Mapping[TDenotation, TNumeral]:
        """Convenience method for accessing ``cls._to_numeral_map`` without type
        errors.

        Returns:
            The mapping from denotation to the numeral representations in the system
        """

        # See project_architecture.md#ClassVars for explanation
        return cls._to_numeral_map

    @classmethod
    def from_numeral_map(cls) -> Mapping[TNumeral, TDenotation]:
        """Convenience method for accessing ``cls._from_numeral_map`` without type
        errors.

        Returns:
            The mapping from the numeral representation in the system to their
                denotation
        """

        # See project_architecture.md#ClassVars for explanation
        return cls._from_numeral_map

    @classmethod
    def _get_base_types(cls, position: int) -> tuple[type, ...]:
        """Returns the base type of the numeral system. When multiple types are
        supported, unfurl the UnionType and return all base types.

        Returns:
            The base type(s) used for numeral representation in the system
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
    def is_valid_numeral(cls, val: Numeral) -> TypeIs[TNumeral]:
        """Checks if a numeral has a valid type for this system."""
        return type(val) in cls._numeral_runtime_type

    @classmethod
    def is_valid_denotation(cls, val: Denotation) -> TypeIs[TDenotation]:
        """Checks if a denotation has a valid type for this system."""
        return type(val) in cls._denotation_runtime_type

    @classmethod
    def _limits(cls, denotation: TDenotation) -> TDenotation:
        """Validates that a denotation is within acceptable limits for the system.

        Args:
            denotation: The denotation to validate

        Returns:
            The validated denotation, replacing the denotation with ``cls.maximum`` if
                the numeral system uses "many" for values at or above the maximum

        Raises:
            ValueError: If the denotation is outside the valid range
        """

        if cls._bounded:
            maximum = cls.maximum

            if denotation < cls.minimum:
                raise ValueError(
                    f"Denotation must be greater or equal to {cls.minimum}."
                )

            if cls.maximum_is_many and denotation > maximum:
                # See project_architecture.md#ClassVars for explanation. Could use
                # cls.is_valid_denotation instead but given ``maximum` is declared
                # on the class this is unnecessary. Ignore the type checker instead.
                return maximum  # pyright: ignore[reportReturnType]

            if denotation > maximum:
                raise ValueError(f"Denotation must be less than or equal to {maximum}.")

        return denotation

    @classmethod
    @abstractmethod
    def _to_numeral(cls, denotation: TDenotation) -> TNumeral:
        """Internal method to convert a denotation to the numeral system's
        representation.

        This method is intended to be implemented by subclasses with the actual
        conversion logic, while the public ``to_numeral`` method handles validation
        and type checking.

        Args:
            denotation: The denotation to convert

        Returns:
            The representation of the denotation in the numeral system

        Raises:
            ValueError: If the denotation is outside the valid range.
        """
        ...

    @classmethod
    def to_numeral(
        cls,
        denotation: TDenotation,
        encode: Literal["utf8", "ascii"] = "utf8",
    ) -> TNumeral:
        """Converts a denotation to the numeral system's representation.

        Args:
            denotation: The denotation to convert

        Returns:
            The representation of the denotation in the numeral system

        Raises:
            ValueError: If the denotation is outside the valid range, or the encoding is
                unsupported
            TypeError: If the denotation cannot be represented in the system
        """

        if not cls.is_valid_denotation(denotation):
            raise TypeError(
                f"{denotation} of type {type(denotation).__name__} cannot be represented in {cls.__name__}."  # noqa: E501
            )

        return cls.to_numeral_trusted(denotation, encode=encode)

    @classmethod
    def to_numeral_trusted(
        cls,
        denotation: TDenotation,
        encode: Literal["utf8", "ascii"] = "utf8",
    ) -> TNumeral:
        """Like ``to_numeral`` but omits the ``is_valid_denotation`` guard.

        Called from ``swop()`` after the caller has already confirmed the denotation
        type via the generic type signature.

        Warning:
            Do not call directly unless the type of ``denotation`` is already validated.

        Args:
            denotation: The denotation to convert

        Returns:
            The representation of the denotation in the numeral system

        Raises:
            ValueError: If the denotation is outside the valid range, or the encoding is
                unsupported
        """
        if encode not in cls.encodings:
            raise ValueError(
                f"Encoding '{encode}' is not supported for {cls.__name__}."
            )

        denotation_: TDenotation = cls._limits(denotation)

        numeral: TNumeral = cls._to_numeral(denotation_)

        if encode == "ascii" and isinstance(numeral, str):
            # See project_architecture.md#ClassVars for explanation. Could use
            # ``cls.is_valid_numeral()``, but given ``encoding` is checked in
            # this method this is unnecessary. Ignore the type checker instead.
            return numeral.translate(ASCII)  # pyright: ignore[reportReturnType]

        return numeral

    @classmethod
    def from_numeral_trusted(cls, numeral: TNumeral) -> TDenotation:
        """Like ``from_numeral`` but omits the ``is_valid_numeral`` guard.

        Called from ``swop()`` after the caller has already confirmed the numeral
        type via the generic type signature.

        Warning:
            Do not call directly unless the type of ``numeral`` is already validated.

        Args:
            numeral: The numeral to convert

        Returns:
            The denotation of the numeral

        Raises:
            ValueError: If the denotation of the numeral is outside the valid range
            ValueError: If the numeral representation is invalid
        """
        denotation: TDenotation = cls._from_numeral(numeral)
        return cls._limits(denotation)

    @classmethod
    @abstractmethod
    def _from_numeral(cls, numeral: TNumeral) -> TDenotation:
        """Internal method to convert a numeral to its denotation.

        This method is intended to be implemented by subclasses with the actual
        conversion logic, while the public ``from_numeral`` method handles validation
        and type checking.

        Args:
            numeral: The numeral to convert.

        Returns:
            The denotation of the numeral.

        Raises:
            ValueError: If the denotation of the numeral is outside the valid range
            ValueError: If the numeral representation is invalid
        """
        ...

    @classmethod
    def from_numeral(
        cls,
        numeral: TNumeral,
    ) -> TDenotation:
        """Converts a numeral representation to its denotation.

        Accepts both UTF-8 and Latin-character forms of numerals unconditionally;
        system maps include entries for both representations.

        Args:
            numeral: The numeral to convert

        Returns:
            The denotation of the numeral

        Raises:
            ValueError: If the denotation of the numeral is outside the valid range
            ValueError: If the numeral representation is invalid
            TypeError: If a denotation in an invalid type is passed to the method.
        """
        if not cls.is_valid_numeral(numeral):
            raise TypeError(
                f"{numeral} of type {type(numeral).__name__} cannot be represented in {cls.__name__}."  # noqa: E501
            )

        denotation: TDenotation = cls._from_numeral(numeral)

        return cls._limits(denotation)
