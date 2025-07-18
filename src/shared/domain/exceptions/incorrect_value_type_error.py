from typing import TypeVar

from src.shared.domain.exceptions.domain_error import DomainError

T = TypeVar("T")


class IncorrectValueTypeError(DomainError):
    def __init__(self, value: T) -> None:
        self._message = f"Value '{value}' is not of type {type(value).__name__}"
        self._type = "incorrect_value_type"
        super().__init__(self._message, self._type)
