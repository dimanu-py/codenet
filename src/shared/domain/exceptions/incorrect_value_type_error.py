from typing import TypeVar

from src.shared.domain.exceptions.domain_error import DomainError

T = TypeVar("T")


class IncorrectValueTypeError(DomainError):
    def __init__(self, value: T) -> None:
        super().__init__(
            message=f"Value '{value}' is not of type {type(value).__name__}",
            error_type="incorrect_value_type",
        )
