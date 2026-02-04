from collections.abc import Callable
from typing import Self, cast

_EMPTY = object()


class Optional[T]:
    __slots__ = ("_value",)

    def __init__(self, value: object = _EMPTY) -> None:
        self._value = value

    @classmethod
    def of(cls, value: T) -> "Optional[T]":
        if value is None:
            raise ValueError("Optional.of(None) is not valid. Use Optional.nothing() instead.")
        return cls(value)

    @classmethod
    def empty(cls) -> "Optional[T]":
        return cls(_EMPTY)

    @classmethod
    def lift[U](cls, value: U | None, mapper: Callable[[U], T]) -> "Optional[T]":
        if value is None:
            return cls.empty()
        return cls.of(mapper(value))

    @classmethod
    def from_nullable(cls, value: T | None) -> "Optional[T]":
        return cls.of(value) if value else cls.empty()

    def is_present(self) -> bool:
        return self._value is not _EMPTY

    def is_empty(self) -> bool:
        return self._value is _EMPTY

    def map[U](self, func: Callable[[T], U]) -> "Optional[U]":
        if self.is_empty():
            return Optional.empty()
        return Optional.of(func(cast(T, self._value)))

    def match[U](self, of: Callable[[T], U], empty: Callable[[], U]) -> U:
        if self.is_empty():
            return empty()
        return of(cast(T, self._value))

    def unwrap(self) -> T:
        if self.is_empty():
            raise ValueError("Cannot unwrap an empty Optional.")
        return cast(T, self._value)

    def unwrap_or_raise(self, error_builder: Callable[[], Exception]) -> T:
        if self.is_empty():
            raise error_builder()
        return cast(T, self._value)

    def __repr__(self) -> str:
        return "Empty" if self.is_empty() else f"Optional({self._value})"

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Optional):
            return False
        return self._value == other._value


def raise_error(exception: Exception) -> None:
    raise exception
