from datetime import datetime, timezone

from expects import equal, expect, raise_error
from sindripy.value_objects import SindriValidationError

from src.auth.account.domain.account_created_at import AccountCreatedAt


class TestAccountCreatedAt:
    def test_should_create_as_datetime_with_utc_timezone(self) -> None:
        value = datetime(2020, 1, 1, tzinfo=timezone.utc)

        created_at = AccountCreatedAt(value)

        expect(created_at.value).to(equal(value))

    def test_should_raise_error_if_value_is_empty(self) -> None:
        empty_value = None

        expect(lambda: AccountCreatedAt(empty_value)).to(raise_error(SindriValidationError))

    def test_should_raise_error_if_value_is_not_datetime(self) -> None:
        not_datetime_value = "2020-01-01T00:00:00Z"

        expect(lambda: AccountCreatedAt(not_datetime_value)).to(raise_error(SindriValidationError))

    def test_should_raise_error_if_value_does_not_have_utc_timezone(self) -> None:
        value_without_utc_timezone = datetime(2020, 1, 1)

        expect(lambda: AccountCreatedAt(value_without_utc_timezone)).to(raise_error(SindriValidationError))