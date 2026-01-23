from typing import ClassVar

from numberology.system import System


class Roman(System[str]):
    from_int_: ClassVar[dict[int, str]] = {
        1_000: "M",
        900: "CM",
        500: "D",
        400: "CD",
        100: "C",
        90: "XC",
        50: "L",
        40: "XL",
        10: "X",
        9: "IX",
        5: "V",
        4: "IV",
        1: "I",
    }
    to_int_: ClassVar[dict[str, int]] = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1_000,
    }

    minimum: ClassVar[int] = 1
    maximum: ClassVar[int] = 3_999

    maximum_is_many: ClassVar[bool] = False

    @staticmethod
    def _limits(number: int) -> int:
        """Validates that a number is within acceptable limits for Roman numerals.

        Checks if the given number falls within the valid range for Roman numeral
        representation (1 to 3999).

        Args:
            number: The number to validate.

        Returns:
            The validated number.

        Raises:
            ValueError: If the number is not in the range 1..3999.

        Examples:
            >>> Roman._limits(1)
            1
            >>> Roman._limits(3999)
            3999
            >>> Roman._limits(0)
            Traceback (most recent call last):
                ...
            ValueError: Number must be between 1 and 3999
            >>> Roman._limits(4000)
            Traceback (most recent call last):
                ...
            ValueError: Number must be between 1 and 3999
        """

        if not (Roman.minimum <= number <= Roman.maximum):
            raise ValueError(
                f"Number must be between {Roman.minimum} and {Roman.maximum}"
            )
        return number

    @staticmethod
    def from_int(number: int) -> str:
        """Converts an integer to a Roman numeral string.

        Takes an integer and converts it to its Roman numeral representation,
        using subtractive notation where appropriate (e.g., IV for 4, IX for 9).

        Args:
            number: The integer to convert, must be between 1 and 3999.

        Returns:
            The Roman numeral string representation of the number.

        Raises:
            ValueError: If the number is outside the valid range.

        Examples:
            >>> Roman.from_int(1)
            'I'
            >>> Roman.from_int(10)
            'X'
            >>> Roman.from_int(4)
            'IV'
            >>> Roman.from_int(9)
            'IX'
            >>> Roman.from_int(42)
            'XLII'
            >>> Roman.from_int(1994)
            'MCMXCIV'
        """
        result: str = ""
        number_ = Roman._limits(number)

        for latin, roman in Roman.from_int_.items():
            while number_ >= latin:
                result += roman
                number_ -= latin

        return result

    @staticmethod
    def to_int(number: str) -> int:
        """Converts a Roman numeral to an integer.

        Takes a Roman numeral and converts it to its integer equivalent,
        properly handling subtractive notation (e.g., IV -> 4, IX -> 9).

        Args:
            number: The Roman numeral to convert.

        Returns:
            The integer representation of the Roman numeral.

        Raises:
            ValueError: If the string contains invalid Roman numerals.

        Examples:
            >>> Roman.to_int('I')
            1
            >>> Roman.to_int('X')
            10
            >>> Roman.to_int('IV')
            4
            >>> Roman.to_int('IX')
            9
            >>> Roman.to_int('XLII')
            42
            >>> Roman.to_int('MCMXCIV')
            1994
            >>> Roman.to_int('i')  # Case insensitive
            1
            >>> Roman.to_int('Z')
            Traceback (most recent call last):
                ...
            ValueError: Invalid Roman character: Z
        """
        total: int = 0
        prev_value: int = 0
        for char in reversed(number.upper()):
            current_value = Roman.to_int_.get(char)
            if current_value is None:
                raise ValueError(f"Invalid Roman character: {char}")
            if current_value < prev_value:
                total -= current_value
            else:
                total += current_value
            prev_value = current_value

        return Roman._limits(total)
