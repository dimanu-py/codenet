from src.contexts.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.contexts.shared.domain.value_objects.value_object import ValueObject


class StringValueObject(ValueObject[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def _validate(self, value: str) -> None:
        super()._validate(value)
        if not isinstance(value, str):
            raise IncorrectValueTypeError
