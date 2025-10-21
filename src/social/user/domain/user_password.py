from typing import Self

from argon2 import PasswordHasher, extract_parameters
from argon2.exceptions import InvalidHash, VerifyMismatchError

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.domain.value_objects.string_value_object import StringValueObject
from src.shared.domain.value_objects.validation import validate


class UserPassword(StringValueObject):
    _hasher: PasswordHasher = PasswordHasher(
        time_cost=2,
        memory_cost=65536,
        parallelism=4,
    )

    @classmethod
    def from_plain_text(cls, password: str) -> Self:
        hashed_password = cls._hasher.hash(password)
        return cls(hashed_password)

    def verify(self, password: str) -> bool:
        try:
            return self._hasher.verify(self._value, password)
        except VerifyMismatchError:
            return False

    @validate
    def _ensure_stored_password_is_hashed(self, value: str) -> None:
        try:
            extract_parameters(value)
        except InvalidHash as error:
            raise CannotStorePlainTextPassword from error


class CannotStorePlainTextPassword(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Cannot store plain text password.",
            error_type="invalid_password_format",
        )
