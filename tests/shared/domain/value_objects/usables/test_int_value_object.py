import pytest
from expects import equal, expect, raise_error

from src.shared.domain.exceptions.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from src.shared.domain.exceptions.invalid_negative_value_error import (
    InvalidNegativeValueError,
)
from src.shared.domain.exceptions.required_value_error import RequiredValueError
from src.shared.domain.value_objects.usables.int_value_object import IntValueObject
from tests.shared.domain.value_objects.mothers.int_primitives_mother import IntPrimitivesMother


@pytest.mark.unit
class TestIntValueObject:
    def test_should_create_int_value_object(self) -> None:
        value = IntPrimitivesMother.any()

        integer = IntValueObject(value)

        expect(integer.value).to(equal(value))

    def test_should_raise_error_when_value_is_none(self) -> None:
        expect(lambda: IntValueObject(None)).to(raise_error(RequiredValueError))

    def test_should_raise_error_when_value_is_not_integer(self) -> None:
        expect(lambda: IntValueObject("123")).to(raise_error(IncorrectValueTypeError))

    def test_should_raise_error_if_int_value_is_negative(self) -> None:
        expect(lambda: IntValueObject(-1)).to(raise_error(InvalidNegativeValueError))

    def test_should_compare_equal_with_same_value(self) -> None:
        common_value = IntPrimitivesMother.any()
        first_integer = IntValueObject(common_value)
        second_integer = IntValueObject(common_value)

        expect(first_integer).to(equal(second_integer))

    def test_should_not_be_equal_with_different_values(self) -> None:
        first_integer = IntValueObject(IntPrimitivesMother.any())
        second_integer = IntValueObject(IntPrimitivesMother.any())

        expect(first_integer).to_not(equal(second_integer))
