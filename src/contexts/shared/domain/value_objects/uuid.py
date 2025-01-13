from uuid import UUID

from src.contexts.shared.domain.exceptions.required_value_error import (
    RequiredValueError,
)
from src.contexts.shared.domain.value_objects.value_object import ValueObject
from src.contexts.shared.domain.exceptions.invalid_id_format_error import (
    InvalidIdFormatError,
)


class Uuid(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        if value is None:
            raise RequiredValueError
        try:
            UUID(value)
        except ValueError:
            raise InvalidIdFormatError
