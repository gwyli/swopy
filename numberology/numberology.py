"""Main converter module for numeral system conversions.

This module provides the Numberology class which serves as the primary interface
for converting numbers between different numeral systems (Roman, Egyptian, Arabic,etc.).
It handles bidirectional conversions by delegating to the appropriate system
implementations.
"""

from typing import overload

from . import systems  # pyright: ignore[reportUnusedImport]
from .system import Numeral, System


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
        >>> converter.convert(42, systems.Arabic, systems.Roman)
        'XLII'
        >>> # Convert from Roman to Egyptian hieroglyphics
        >>> converter.convert('XLII', systems.Roman, systems.Egyptian)
        '\U00013386\U00013386\U00013386\U00013386\U000133fa\U000133fa'
    """

    @overload
    def convert(
        self, number: Numeral, from_system: System[Numeral], to_system: System[int]
    ) -> int: ...

    @overload
    def convert(
        self, number: Numeral, from_system: System[Numeral], to_system: System[str]
    ) -> str: ...

    def convert(
        self,
        number: Numeral,
        from_system: System[Numeral],
        to_system: System[str] | System[int],
    ) -> Numeral:
        """Converts a number from one numeral system to another.

        Converts a number represented in one numeral system (source) to another
        numeral system (target). Supports both string and integer representations.

        Args:
            number: The number to convert, either as an integer or string.
            from_system: The source numeral system (systems.Arabic or systems.Egyptian).
            to_system: The target numeral system (systems.Arabic or systems.Egyptian).

        Returns:
            The converted number as a string if to_system uses string representation,
            otherwise as an integer.

        Raises:
            ValueError: If the number is outside the valid range for either system.

        Examples:
            >>> converter = Numberology()
            >>> converter.convert(10, systems.Arabic, systems.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.Roman, systems.Egyptian)
            '\U00013386'
            >>> converter.convert('X', systems.Roman, systems.Roman)
            'X'
        """
        intermediate = self._convert_to_int(number, from_system)

        return self._convert_from_int(intermediate, to_system)

    def _convert_to_int(self, number: Numeral, system: System[Numeral]) -> int:
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
            >>> converter._convert_to_int('X', systems.Roman)
            10
            >>> converter._convert_to_int('\U00013386', systems.Egyptian)
            10
        """
        if isinstance(number, int):
            return number

        return system.to_int(number)

    def _convert_from_int(
        self, number: Numeral, system: System[str] | System[int]
    ) -> Numeral:
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
            >>> converter._convert_from_int(10, systems.Roman)
            'X'
            >>> converter._convert_from_int(10, systems.Egyptian)
            '\U00013386'
        """
        if isinstance(number, str):
            return number

        return system.from_int(number)

    @staticmethod
    def get_all_systems() -> dict[str, type[System[Numeral]]]:
        """Discovers and returns all available numeral system classes.

        Provides easy discovery of all supported numeral systems without
        requiring knowledge of the systems module structure.

        Returns:
            A dictionary mapping system names to their corresponding System classes.
            Keys are the class names (e.g., 'Roman', 'Egyptian'), values are the
            System subclasses.

        Examples:
            >>> converter = Numberology()
            >>> all_systems = converter.get_all_systems()
            >>> 'Roman' in all_systems
            True
            >>> 'Arabic' in all_systems
            True

            Get system properties:
            >>> all_systems = Numberology.get_all_systems()
            >>> roman = all_systems['Roman']
            >>> roman.minimum
            1
            >>> roman.maximum
            3999
        """
        result: dict[str, type[System[Numeral]]] = {}

        for name in getattr(systems, "__all__", []):
            system_class = getattr(systems, name)
            if isinstance(system_class, type) and issubclass(system_class, System):
                result[name] = system_class

        return result
