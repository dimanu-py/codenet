from typing import Self

from argon2 import PasswordHasher

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.domain.value_objects.string_value_object import StringValueObject


class UserPassword(StringValueObject):
    @classmethod
    def from_plain_text(cls, password: str) -> Self:
        hasher = PasswordHasher(
            time_cost=2,
            memory_cost=65536,
            parallelism=4,
        )
        hashed_password = hasher.hash(password)
        return cls(hashed_password)


class CannotStorePlainTextPassword(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Cannot store plain text password.",
            error_type="invalid_password_format",
        )
