from typing import ClassVar, TypeVar

T = TypeVar("T", str, int)


class System[T]:
    from_int_: ClassVar[list[tuple[int, str]]]
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
