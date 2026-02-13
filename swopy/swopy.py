"""Main module for numeral system conversions.

This module provides the swopy() method which serves as the primary interface
for converting numbers between different numeral systems (Roman, Egyptian, Arabic, etc.)
It handles bidirectional conversions by delegating to the appropriate system
implementations.
"""

from inspect import getmembers, isclass
from typing import Any

from . import systems
from .system import Denotation, Numeral, System


def swop[
    TFromNumeral: Numeral,
    TFromDenotation: Denotation,
    TToNumeral: Numeral,
    TToDenotation: Denotation,
](
    number: TFromNumeral,
    from_system: type[System[TFromNumeral, TFromDenotation]],
    to_system: type[System[TToNumeral, TToDenotation]],
) -> TToNumeral:
    """Universal converter for numeral system transformations.

    Provides a simple interface to convert numbers between different numeral
    systems. Validates input against both source and target system constraints,
    then performs the conversion via Arabic numerals.

    Args:
        number: The number to convert, in whatever format the source system accepts.
        from_system: The source numeral system.
        to_system: The target numeral system.

    Returns:
        The number in the target numeral system in an appropriate type based on the
        system's implementation.

    Raises:
        ValueError: If the number is outside the valid range for either system.
        TypeError: If the number cannot be represented in the target system.

    Examples:
        >>> swop(10, systems.arabic.Arabic, systems.egyptian.Egyptian)
        '\U00013386'
        >>> swop('X', systems.roman.Standard, \
            systems.egyptian.Egyptian)
        '\U00013386'
        >>> swop('X', systems.roman.Standard, systems.roman.Standard)
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
