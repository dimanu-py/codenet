from uuid import UUID

from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.value_objects.value_object import ValueObject
from src.shared.domain.exceptions.invalid_id_format_error import InvalidIdFormatError


class Uuid(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise IncorrectValueTypeError
        try:
            UUID(value)
        except ValueError:
            raise InvalidIdFormatError
