import pytest
from expects import expect, be_true

from src.shared.domain.value_objects.optional import Optional
from src.shared.domain.value_objects.string_value_object import StringValueObject


@pytest.mark.unit
class TestOptionalBasicConstructor:
    def test_should_be_able_to_create_optional_with_valid_value(self) -> None:
        value = StringValueObject("test")

        optional = Optional.of(value)

        expect(optional.is_present()).to(be_true)
