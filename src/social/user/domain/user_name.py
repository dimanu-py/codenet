import re

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class UserName(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z.\- áéíóúÁÉÍÓÚñÑüÜäÄöÖëËïÏç'\s]+$"

    @validate
    def _ensure_name_has_valid_characters(self, value: str) -> None:
        if re.match(self.CORRECT_CHARACTERS, value) is None:
            raise InvalidNameFormatError


class InvalidNameFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Name cannot contain special characters or numbers.",
            error_type="invalid_name_format",
        )
