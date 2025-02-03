from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_negative_value_error import (
    InvalidNegativeValueError,
)
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.value_object import ValueObject


class IntValueObject(ValueObject[int]):
    def _validate(self, value: int) -> None:
        if value is None:
            raise RequiredValueError
        if not isinstance(value, int):
            raise IncorrectValueTypeError
        if value < 0:
            raise InvalidNegativeValueError(value)
