from abc import ABC
from typing import override

from src.contexts.shared.domain.exceptions.required_value_error import (
    RequiredValueError,
)


class ValueObject[T](ABC):
    _value: T

    def __init__(self, value: T) -> None:
        self._validate(value)
        self._value = value

    def _validate(self, value: T) -> None:
        if value is None:
            raise RequiredValueError

    @property
    def value(self) -> T:
        return self._value

    @override
    def __eq__(self, other: "ValueObject[T]") -> bool:
        return self.value == other.value
