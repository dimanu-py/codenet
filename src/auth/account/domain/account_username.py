import re

from src.shared.domain.exceptions.domain_error import ConflictError, DomainValidationError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class AccountUsername(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z0-9_.]+$"

    @validate
    def _ensure_name_has_valid_characters(self) -> None:
        if re.match(self.CORRECT_CHARACTERS, self._value) is None:
            raise InvalidUsernameFormat


class InvalidUsernameFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="Username cannot contain special characters",
            error_type="account_validation_error",
        )


class AccountUsernameAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            message="Username is already registered.",
            error_type="account_resource_conflict_error",
        )
