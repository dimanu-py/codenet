from uuid import UUID

from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_id_format_error import InvalidIdFormatError
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.value_object import ValueObject


class Uuid(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        if value is None:
            raise RequiredValueError
        if not isinstance(value, str):
            raise IncorrectValueTypeError(value)
        try:
            UUID(value)
        except ValueError:
            raise InvalidIdFormatError
