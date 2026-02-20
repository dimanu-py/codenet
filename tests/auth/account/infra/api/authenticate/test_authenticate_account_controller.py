from unittest.mock import ANY

import pytest
from expects import expect, equal

from src.auth.account.infra.api.authenticate.authenticate_account_controller import AuthenticateAccountController
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestSignupAccountController:
    _response = None
    _ANY_EMAIL = AccountEmailPrimitivesMother.any()
    _ANY_PASSWORD = AccountPasswordHashPrimitivesMother.any()

    def setup_method(self) -> None:
        self._controller = AuthenticateAccountController()

    async def test_should_return_200_when_authenticating_account_successfully(self) -> None:
        self._should_authenticate_account()

        self._response = await self._controller.authenticate(
            identification=self._ANY_EMAIL, password=self._ANY_PASSWORD
        )

        self._assert_contract_is_met_on_success(
            200,
            {"access_token": ANY, "token_type": "bearer", "expires_in": ANY},
        )

    def _should_authenticate_account(self) -> None:
        pass

    def _assert_contract_is_met_on_success(self, expected_status_code: int, expected_body: dict[str, str]) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.data).to(equal(expected_body))
