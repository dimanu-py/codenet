from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_negative_value_error import (
    InvalidNegativeValueError,
)
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.value_object import ValueObject


class IntValueObject(ValueObject[int]):
    def __init__(self, value: int) -> None:
        super().__init__(value)

    def _validate(self) -> None:
        if self._value is None:
            raise RequiredValueError
        if not isinstance(self._value, int):
            raise IncorrectValueTypeError
        if self._value < 0:
            raise InvalidNegativeValueError(self._value)
