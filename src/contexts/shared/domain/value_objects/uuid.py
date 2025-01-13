from uuid import UUID

from src.contexts.shared.domain.exceptions.invalid_id_format_error import (
    InvalidIdFormatError,
)
from src.contexts.shared.domain.value_objects.value_object import ValueObject


class Uuid(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        super()._validate(value)
        try:
            UUID(value)
        except ValueError:
            raise InvalidIdFormatError
