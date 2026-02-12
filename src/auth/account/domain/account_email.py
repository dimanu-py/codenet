import re

from src.shared.domain.exceptions.domain_error import DomainValidationError
from src.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.shared.domain.value_objects.validation import validate


class AccountEmail(StringValueObject):
    EMAIL_FORMAT = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @validate
    def _ensure_email_has_correct_format(self) -> None:
        if re.match(self.EMAIL_FORMAT, self._value) is None:
            raise InvalidEmailFormat


class InvalidEmailFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="Email cannot contain special characters and must contain '@' and '.'",
            error_type="account_validation_error",
        )
