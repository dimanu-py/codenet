import pytest
from expects import expect, be_true, raise_error

from src.shared.domain.value_objects.optional import Optional
from src.shared.domain.value_objects.string_value_object import StringValueObject


@pytest.mark.unit
class TestOptionalBasicConstructor:
    def test_should_be_able_to_create_optional_with_valid_value(self) -> None:
        value = StringValueObject("test")

        optional = Optional.of(value)

        expect(optional.is_present()).to(be_true)

    def test_should_raise_error_when_creating_optional_with_invalid_value(self) -> None:
        empty_value = None

        expect(lambda: Optional.of(empty_value)).to(raise_error(ValueError))
