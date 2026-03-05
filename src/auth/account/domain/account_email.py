import re

from sindripy.value_objects import String, validate

from src.shared.domain.exceptions.domain_error import ConflictError, DomainValidationError


class AccountEmail(String):
    EMAIL_FORMAT = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @validate
    def _ensure_email_has_correct_format(self) -> None:
        if re.match(self.EMAIL_FORMAT, self._value) is None:
            raise InvalidEmailFormat


class InvalidEmailFormat(DomainValidationError):
    def __init__(self) -> None:
        super().__init__(message="Email cannot contain special characters and must contain '@' and '.'")


class AccountEmailAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(message="Email is already signed up")
