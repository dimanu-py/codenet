from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_negative_value_error import (
    InvalidNegativeValueError,
)
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.decorators.validation import validate
from src.shared.domain.value_objects.value_object import ValueObject


class IntValueObject(ValueObject[int]):
    @validate
    def _ensure_has_value(self, value: int) -> None:
        if value is None:
            raise RequiredValueError

    @validate
    def _ensure_value_is_integer(self, value: int) -> None:
        if not isinstance(value, int):
            raise IncorrectValueTypeError(value)

    @validate
    def _ensure_value_is_positive(self, value: int) -> None:
        if value < 0:
            raise InvalidNegativeValueError(value)
