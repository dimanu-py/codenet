from abc import ABC, abstractmethod
from typing import override, Self


class ValueObject[T](ABC):
    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    _value: T

    def __init__(self, value: T) -> None:
        self._validate(value)
        object.__setattr__(self, "_value", value)

    @abstractmethod
    def _validate(self, value: T) -> None: ...

    @property
    def value(self) -> T:
        return self._value

    @override
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value!r})"

    @override
    def __str__(self) -> str:
        return str(self._value)

    @override
    def __setattr__(self, name: str, value: T) -> None:
        """Prevents modification of the value after initialization."""
        if name in self.__slots__:
            raise AttributeError("Cannot modify the value of a ValueObject")

        public_name = name.replace("_", "")
        public_slots = [slot.replace("_", "") for slot in self.__slots__]
        if public_name in public_slots:
            raise AttributeError("Cannot modify the value of a ValueObject")

        raise AttributeError(
            f"Class {self.__class__.__name__} object has no attribute '{name}'"
        )
