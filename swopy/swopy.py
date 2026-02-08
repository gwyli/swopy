"""Main converter module for numeral system conversions.

This module provides the Swopy class which serves as the primary interface
for converting numbers between different numeral systems (Roman, Egyptian, Arabic,etc.).
It handles bidirectional conversions by delegating to the appropriate system
implementations.
"""

from inspect import getmembers, isclass
from typing import Any

from . import systems
from .system import Denotation, Numeral, System


class Swopy:
    """Universal converter for numeral system transformations.

    Provides a simple interface to convert numbers between different numeral
    systems. The converter validates input against both source and target system
    constraints, then performs the conversion via an intermediate integer
    representation.

    The Swopy class acts as a facade that coordinates between different
    numeral system implementations, handling both string and integer input types
    and returning results in the appropriate format for the target system.

    Examples:
        >>> converter = Swopy()
        >>> # Convert from Arabic to Roman numerals
        >>> converter.convert(42, systems.arabic.Arabic, systems.roman.Standard)
        'XLII'
        >>> # Convert from Roman to Egyptian hieroglyphics
        >>> converter.convert('XLII', systems.roman.Standard, systems.egyptian.Egyptian)
        '\U00013386\U00013386\U00013386\U00013386\U000133fa\U000133fa'
    """

    def convert[
        TFromNumeral: Numeral,
        TFromDenotation: Denotation,
        TToNumeral: Numeral,
        TToDenotation: Denotation,
    ](
        self,
        number: TFromNumeral,
        from_system: type[System[TFromNumeral, TFromDenotation]],
        to_system: type[System[TToNumeral, TToDenotation]],
    ) -> TToNumeral:
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
            >>> converter = Swopy()
            >>> converter.convert(10, systems.arabic.Arabic, systems.egyptian.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.roman.Standard, \
                systems.egyptian.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.roman.Standard, systems.roman.Standard)
            'X'
        """

        intermediate: TFromDenotation = from_system.from_numeral(number)

        if to_system.is_valid_denotation(intermediate):
            return to_system.to_numeral(intermediate)

        raise TypeError(
            f"{number} of type {type(number)} cannot be represented in {to_system.__name__}."  # noqa: E501
        )


def get_all_systems() -> dict[str, type[System[Any, Any]]]:
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
    result: dict[str, type[System[Any, Any]]] = {}

    for module_name in getattr(systems, "__all__", []):
        module = getattr(systems, module_name)

        for _, obj in getmembers(module):
            if isclass(obj) and issubclass(obj, System):
                if obj.__name__ == "System":
                    continue
                result[f"{obj.__module__.split('.')[-1]}.{obj.__name__}"] = obj

    return result
