from typing import override

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

    @override
    def __init__(self, value: str) -> None:
        if self._is_already_hashed(value):
            super().__init__(value)
        else:
            super().__init__(self._hash_plain_password(value))

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

    def _hash_plain_password(self, value: str) -> str:
        return self._hasher.hash(value)

    @staticmethod
    def _is_already_hashed(value: str) -> bool:
        try:
            extract_parameters(value)
            return True
        except InvalidHash:
            return False


class CannotStorePlainTextPassword(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Cannot store plain text password.",
            error_type="invalid_password_format",
        )
