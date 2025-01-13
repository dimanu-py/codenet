import validators

from src.contexts.shared.domain.value_objects.string_value_object import (
    StringValueObject,
)
from src.contexts.social.user.domain.invalid_url_format_error import (
    InvalidUrlFormatError,
)


class UserProfilePicture(StringValueObject):
    VALID_FORMATS = (".jpg", ".jpeg", ".png")

    def _validate(self, value: str) -> None:
        super()._validate(value)
        self._ensure_url_image_is_valid(value)

    def _ensure_url_image_is_valid(self, value: str) -> None:
        is_invalid_url = isinstance(validators.url(value), validators.ValidationError)
        has_invalid_extension = not value.endswith(self.VALID_FORMATS)

        if is_invalid_url or has_invalid_extension:
            raise InvalidUrlFormatError
