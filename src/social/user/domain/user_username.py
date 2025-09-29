import re

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.domain.value_objects.decorators.validation import validate
from src.shared.domain.value_objects.usables.string_value_object import (
    StringValueObject,
)


class UserUsername(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z0-9_.]+$"

    @validate
    def _ensure_name_has_valid_characters(self, value: str) -> None:
        if re.match(self.CORRECT_CHARACTERS, value) is None:
            raise InvalidUsernameFormatError


class InvalidUsernameFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Username cannot contain special characters",
            error_type="invalid_username_format",
        )
