import re

from sindripy.value_objects import String, validate

from src.shared.domain.exceptions.domain_error import ConflictError, DomainValidationError


class AccountUsername(String):
    CORRECT_CHARACTERS = r"^[a-zA-Z0-9_.]+$"

    @validate
    def _ensure_name_has_valid_characters(self) -> None:
        if re.match(self.CORRECT_CHARACTERS, self._value) is None:
            raise InvalidUsernameFormat


class InvalidUsernameFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(message="Username cannot contain special characters")


class AccountUsernameAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(message="Username is already registered.")
