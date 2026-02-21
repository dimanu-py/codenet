from unittest.mock import AsyncMock

import pytest
from expects import expect, equal

from src.auth.account.application.authenticate.account_authenticator import AccountAuthenticator, InvalidCredentials
from src.auth.account.infra.api.authenticate.authenticate_account_controller import AuthenticateAccountController
from src.auth.account.infra.authentication_token import AuthenticationToken
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
        self._authenticator = AsyncMock(spect=AccountAuthenticator)
        self._controller = AuthenticateAccountController(use_case=self._authenticator)

    async def test_should_return_200_when_authenticating_account_successfully(self) -> None:
        token = self._should_authenticate_account()

        self._response = await self._controller.authenticate(
            identification=self._ANY_EMAIL, password=self._ANY_PASSWORD
        )

        self._assert_contract_is_met_on_success(
            200,
            token,
        )

    async def test_should_return_401_when_account_authenticates_with_invalid_credentials(self) -> None:
        self._should_fail_authenticating_account_with_invalid_credentials()

        self._response = await self._controller.authenticate(identification="wrong_email", password=self._ANY_PASSWORD)

        self._assert_contract_is_met_on_error(401)

    def _should_authenticate_account(self) -> AuthenticationToken:
        token = AuthenticationToken(access_token="any", token_type="bearer", expires_in=3600, )
        self._authenticator.execute.return_value = token
        return token

    def _should_fail_authenticating_account_with_invalid_credentials(self) -> None:
        self._authenticator.execute.side_effect = InvalidCredentials()

    def _assert_contract_is_met_on_success(self, expected_status_code: int, expected_body: dict[str, str]) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.data).to(equal(expected_body))

    def _assert_contract_is_met_on_error(self, expected_status_code: int) -> None:
        expect(self._response.status).to(equal(expected_status_code))
