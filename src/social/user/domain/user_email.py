import re

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class UserEmail(StringValueObject):
    EMAIL_FORMAT = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @validate
    def _ensure_email_has_correct_format(self, value: str) -> None:
        if re.match(self.EMAIL_FORMAT, value) is None:
            raise InvalidEmailFormatError


class InvalidEmailFormatError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Email cannot contain special characters and must contain '@' and '.'",
            error_type="invalid_email_format",
        )
