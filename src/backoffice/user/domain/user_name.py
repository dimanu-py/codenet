import re

from sindripy.value_objects import String, validate

from src.shared.domain.exceptions.domain_error import DomainValidationError


class UserName(String):
    CORRECT_CHARACTERS = r"^[a-zA-Z.\- áéíóúÁÉÍÓÚñÑüÜäÄöÖëËïÏç'\s]+$"

    @validate
    def _ensure_name_has_valid_characters(self) -> None:
        if re.match(self.CORRECT_CHARACTERS, self._value) is None:
            raise InvalidNameFormat


class InvalidNameFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="Name cannot contain special characters or numbers.",
            error_type="user_validation_error",
        )
