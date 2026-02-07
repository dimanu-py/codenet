import re

from src.shared.domain.exceptions.domain_validation_error import DomainValidationError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class UserUsername(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z0-9_.]+$"

    @validate
    def _ensure_name_has_valid_characters(self, value: str) -> None:
        if re.match(self.CORRECT_CHARACTERS, value) is None:
            raise InvalidUsernameFormat


class InvalidUsernameFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="Username cannot contain special characters",
            error_type="invalid_username_format",
        )
