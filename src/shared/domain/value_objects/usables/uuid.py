from uuid import UUID

from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_id_format_error import InvalidIdFormatError
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.decorators.validation import validate
from src.shared.domain.value_objects.value_object import ValueObject


class Uuid(ValueObject[str]):
    @validate
    def _ensure_has_value(self, value: str) -> None:
        if value is None:
            raise RequiredValueError

    @validate
    def _ensure_value_is_string(self, value: str) -> None:
        if not isinstance(value, str):
            raise IncorrectValueTypeError(value)

    @validate
    def _ensure_value_has_valid_uuid_format(self, value: str) -> None:
        try:
            UUID(value)
        except ValueError as error:
            raise InvalidIdFormatError from error
