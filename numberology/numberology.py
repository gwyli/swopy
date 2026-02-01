"""Main converter module for numeral system conversions.

This module provides the Numberology class which serves as the primary interface
for converting numbers between different numeral systems (Roman, Egyptian, Arabic,etc.).
It handles bidirectional conversions by delegating to the appropriate system
implementations.
"""

from fractions import Fraction
from inspect import getmembers, isclass
from typing import Any, TypeVar

from . import systems
from .system import RealNumber, System

TFromType = TypeVar("TFromType", RealNumber, Fraction | int, int, str)
TToType = TypeVar("TToType", RealNumber, Fraction | int, int, str)


class Numberology:
    """Universal converter for numeral system transformations.

    Provides a simple interface to convert numbers between different numeral
    systems. The converter validates input against both source and target system
    constraints, then performs the conversion via an intermediate integer
    representation.

    The Numberology class acts as a facade that coordinates between different
    numeral system implementations, handling both string and integer input types
    and returning results in the appropriate format for the target system.

    Examples:
        >>> converter = Numberology()
        >>> # Convert from Arabic to Roman numerals
        >>> converter.convert(42, systems.arabic.Arabic, systems.roman.Standard)
        'XLII'
        >>> # Convert from Roman to Egyptian hieroglyphics
        >>> converter.convert('XLII', systems.roman.Standard, systems.egyptian.Egyptian)
        '\U00013386\U00013386\U00013386\U00013386\U000133fa\U000133fa'
    """

    def convert(
        self,
        number: TFromType,
        from_system: type[System[TFromType]],
        to_system: type[System[TToType]],
    ) -> TToType:
        # FIXME: Add a type guard to ensure a fraction isn't implicitly converted to int
        """Converts a number from one numeral system to another.

        Converts a number represented in one numeral system (source) to another
        numeral system (target). Supports both string and integer representations.

        Args:
            number: The number to convert, either as an integer or string.
            from_system: The source numeral system (systems.arabic.Arabic or
                systems.egyptian.Egyptian).
            to_system: The target numeral system (systems.arabic.Arabic or
                systems.egyptian.Egyptian).

        Returns:
            The converted number as a string if to_system uses string representation,
            otherwise as an integer.

        Raises:
            ValueError: If the number is outside the valid range for either system.

        Examples:
            >>> converter = Numberology()
            >>> converter.convert(10, systems.arabic.Arabic, systems.egyptian.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.roman.Standard, \
                systems.egyptian.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.roman.Standard, systems.roman.Standard)
            'X'
        """

        intermediate: RealNumber = self._convert_from_numeral(number, from_system)

        return self._convert_to_numeral(intermediate, to_system)

    def _convert_from_numeral(
        self, number: TFromType, system: type[System[TFromType]]
    ) -> RealNumber:
        """Converts a number to an integer representation.

        Takes a number in either string or integer form and returns its integer
        equivalent in the provided system.

        Args:
            number: The number to convert, either as an integer or string.
            module: The numeral system to use.

        Returns:
            The integer representation of the number.

        Examples:
            >>> converter = Numberology()
            >>> converter._convert_from_numeral('X', systems.roman.Standard)
            10
            >>> converter._convert_from_numeral('\U00013386', systems.egyptian.Egyptian)
            10
        """
        if isinstance(number, int):
            return number

        return system.from_numeral(number)

    def _convert_to_numeral(
        self, number: RealNumber, system: type[System[TToType]]
    ) -> TToType:
        """Converts an integer to the string representation of a numeral system,
        unless the system uses Arabic numerals.

        Args:
            number: The number to convert, either as an integer or string.
            system: The numeral system.

        Returns:
            The string representation of the number in the target system.

        Examples:
            >>> converter = Numberology()
            >>> from . import systems
            >>> converter._convert_to_numeral(10, systems.roman.Standard)
            'X'
            >>> converter._convert_to_numeral(10, systems.egyptian.Egyptian)
            '\U00013386'
        """

        return system.to_numeral(number)


def get_all_systems() -> dict[str, type[System[Any]]]:
    """Discovers and returns all available numeral system classes.

    Provides easy discovery of all supported numeral systems without
    requiring knowledge of the systems module structure.

    Returns:
        A dictionary mapping system names to their corresponding System classes.
        Keys are the class names (e.g., 'Roman', 'Egyptian'), values are the
        System subclasses.

    Examples:
        >>> all_systems = get_all_systems()
        >>> 'roman.Standard' in all_systems
        True
        >>> 'arabic.Arabic' in all_systems
        True

        Get system properties:
        >>> all_systems = get_all_systems()
        >>> roman = all_systems['roman.Standard']
        >>> roman.minimum
        1
        >>> roman.maximum
        3999
    """
    result: dict[str, type[System[Any]]] = {}

    for module_name in getattr(systems, "__all__", []):
        module = getattr(systems, module_name)

        for _, obj in getmembers(module):
            if isclass(obj) and issubclass(obj, System):
                if obj.__name__ == "System":
                    continue
                result[f"{obj.__module__.split('.')[-1]}.{obj.__name__}"] = obj

    return result
