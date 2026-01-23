from enum import Enum

from . import systems


class System(Enum):
    EGYPTIAN = systems.egyptian
    ARABIC = systems.arabic
    ROMAN = systems.roman


class Numberology:
    def convert(
        self, number: int | str, from_system: System, to_system: System
    ) -> str | int:
        """Converts a number from one numeral system to another.

        Converts a number represented in one numeral system (source) to another
        numeral system (target). Supports both string and integer representations.

        Args:
            number: The number to convert, either as an integer or string.
            from_system: The source numeral system (System.ARABIC or System.EGYPTIAN).
            to_system: The target numeral system (System.ARABIC or System.EGYPTIAN).

        Returns:
            The converted number as a string if to_system uses string representation,
            otherwise as an integer.

        Raises:
            ValueError: If the number is outside the valid range for either system.

        Examples:
            >>> converter = Numberology()
            >>> converter.convert(10, System.ARABIC, System.EGYPTIAN)
            '\U00013386'
            >>> converter.convert('X', System.ROMAN, System.EGYPTIAN)
            '\U00013386'
        """
        intermediate = self._convert_to_int(number, from_system)

        return self._convert_from_int(intermediate, to_system)

    def _convert_to_int(self, number: str | int, system: System) -> int:
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
            >>> converter._convert_to_int('X', System.ROMAN)
            10
            >>> converter._convert_to_int('\U00013386', System.EGYPTIAN)
            10
        """
        if isinstance(number, int):
            return number

        return system.value.to_int(number)

    def _convert_from_int(self, number: str | int, system: System) -> str | int:
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
            >>> converter._convert_from_int(10, System.ROMAN)
            'X'
            >>> converter._convert_from_int(10, System.EGYPTIAN)
            '\U00013386'
        """
        if isinstance(number, str):
            return number

        return system.value.from_int(number)
