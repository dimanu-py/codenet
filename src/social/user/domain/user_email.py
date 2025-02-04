import re

from src.shared.domain.value_objects.string_value_object import StringValueObject
from src.social.user.domain.invalid_email_format_error import InvalidEmailFormatError


class UserEmail(StringValueObject):
    EMAIL_FORMAT = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def _validate(self, value: str) -> None:
        super()._validate(value)
        self._ensure_email_has_correct_format(value)

    def _ensure_email_has_correct_format(self, value: str) -> None:
        if re.match(self.EMAIL_FORMAT, value) is None:
            raise InvalidEmailFormatError
