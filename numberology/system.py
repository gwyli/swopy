from abc import ABC, abstractmethod
from sys import maxsize
from typing import ClassVar


class System[T: str | int](ABC):
    from_int_: ClassVar[dict[int, str]]
    to_int_: ClassVar[dict[str, int]]

    minimum: ClassVar[int] = -maxsize
    maximum: ClassVar[int] = maxsize
    maximum_is_many: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def _limits(cls, number: int) -> int: ...

    @classmethod
    @abstractmethod
    def from_int(cls, number: int) -> str | int: ...

    @classmethod
    @abstractmethod
    def to_int(cls, number: T) -> int: ...
