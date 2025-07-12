import re

from src.shared.domain.value_objects.decorators.validation import validate
from src.shared.domain.value_objects.usables.string_value_object import StringValueObject
from src.social.user.domain.invalid_email_format_error import InvalidEmailFormatError


class UserEmail(StringValueObject):
    EMAIL_FORMAT = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    @validate
    def _ensure_email_has_correct_format(self, value: str) -> None:
        if re.match(self.EMAIL_FORMAT, value) is None:
            raise InvalidEmailFormatError
