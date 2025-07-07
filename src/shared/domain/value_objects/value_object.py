from abc import ABC, abstractmethod
from typing import override, Self


class ValueObject[T](ABC):
    _value: T

    def __init__(self, value: T) -> None:
        self._value = value
        self._validate()

    @abstractmethod
    def _validate(self) -> None: ...

    @property
    def value(self) -> T:
        return self._value

    @override
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value
