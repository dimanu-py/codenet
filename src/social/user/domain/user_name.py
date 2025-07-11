import re

from src.shared.domain.value_objects.string_value_object import StringValueObject
from src.social.user.domain.invalid_name_format_error import InvalidNameFormatError


class UserName(StringValueObject):
    CORRECT_CHARACTERS = r"^[a-zA-Z.\- áéíóúÁÉÍÓÚñÑüÜäÄöÖëËïÏç'\s]+$"

    def _validate(self, value: str) -> None:
        super()._validate(value)
        self._ensure_name_has_valid_characters(value)

    def _ensure_name_has_valid_characters(self, value: str) -> None:
        if re.match(self.CORRECT_CHARACTERS, value) is None:
            raise InvalidNameFormatError
