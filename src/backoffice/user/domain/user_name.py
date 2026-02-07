import re

from src.shared.domain.exceptions.domain_validation_error import DomainValidationError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class UserName(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z.\- áéíóúÁÉÍÓÚñÑüÜäÄöÖëËïÏç'\s]+$"

    @validate
    def _ensure_name_has_valid_characters(self) -> None:
        if re.match(self.CORRECT_CHARACTERS, self._value) is None:
            raise InvalidNameFormat


class InvalidNameFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="Name cannot contain special characters or numbers.",
            error_type="invalid_name_format",
        )
