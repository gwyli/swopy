from typing import ClassVar

from pydantic import BaseModel


class System[T: str | int](BaseModel):
    from_int_: ClassVar[dict[int, str]]
    to_int_: ClassVar[dict[str, int]]

    minimum: ClassVar[int]
    maximum: ClassVar[int]
    maximum_is_many: ClassVar[bool]

    @staticmethod
    def _limits(number: int) -> int: ...

    @staticmethod
    def from_int(number: int) -> str | int: ...

    @staticmethod
    def to_int(number: T) -> int: ...
