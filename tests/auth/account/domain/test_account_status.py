import pytest
from expects import equal, expect, raise_error

from src.auth.account.domain.account_status import AccountStatus, AccountStatusDoesNotExists


@pytest.mark.unit
class TestAccountStatus:
    def test_should_store_valid_status(self) -> None:
        status = "active"

        account_status = AccountStatus(status)

        expect(account_status.value).to(equal(status))

    def test_should_raise_error_when_status_does_not_exist(self) -> None:
        invalid_status = "invalid_status"

        expect(lambda: AccountStatus(invalid_status)).to(raise_error(AccountStatusDoesNotExists))
