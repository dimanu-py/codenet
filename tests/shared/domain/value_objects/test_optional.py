import pytest
from expects import expect, be_true, raise_error, equal

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

    def test_should_be_able_to_create_empty_optional(self) -> None:
        optional = Optional.empty()

        expect(optional.is_empty()).to(be_true)

    def test_should_return_value_when_unwrapping_present_optional(self) -> None:
        value = "test_value"
        optional = Optional.of(value)

        stored_value = optional.unwrap()

        expect(stored_value).to(equal(value))

    def test_should_raise_error_when_unwrapping_empty(self) -> None:
        optional = Optional.empty()

        expect(lambda: optional.unwrap()).to(raise_error(ValueError))

    def test_should_return_empty_when_mapping_empty(self) -> None:
        optional = Optional.empty()

        result = optional.map(lambda value: value.upper())

        expect(result.is_empty()).to(be_true)

    def test_should_transform_present_value_with_map(self) -> None:
        optional = Optional.of("hello")

        result = optional.map(lambda value: value.upper())

        expect(result.unwrap()).to(equal("HELLO"))

    def test_should_raise_error_when_map_function_returns_none(self) -> None:
        optional = Optional.of("test")

        expect(lambda: optional.map(lambda x: None)).to(raise_error(ValueError))

    def test_should_raise_custom_error_when_unwrap_or_raise_on_empty(self) -> None:
        optional = Optional.empty()

        expect(lambda: optional.unwrap_or_raise(lambda: RuntimeError("Custom error message"))).to(raise_error(RuntimeError, "Custom error message"))

    def test_should_return_value_when_unwrap_or_raise_on_present_optional(self) -> None:
        value = "test_value"
        optional = Optional.of(value)

        result = optional.unwrap_or_raise(lambda: RuntimeError("Should not be called"))

        expect(result).to(equal(value))

    def test_should_handle_complex_objects(self) -> None:
        complex_value = {"key": "value", "nested": {"data": 42}}
        optional = Optional.of(complex_value)

        result = optional.map(lambda x: x["nested"]["data"])

        expect(result.unwrap()).to(equal(42))

    def test_should_chain_multiple_operations(self) -> None:
        optional = Optional.of("  hello world  ")

        result = optional.map(str.strip).map(lambda value: value.upper()).map(lambda value: value.split())

        expect(result.unwrap()).to(equal(["HELLO", "WORLD"]))
