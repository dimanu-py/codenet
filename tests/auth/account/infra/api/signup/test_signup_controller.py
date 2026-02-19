from unittest.mock import AsyncMock

import pytest
from expects import equal, expect

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.delivery.signup.signup_account_request import SignupAccountRequest
from src.auth.account.domain.account_email import AccountEmailAlreadyExists
from src.auth.account.domain.account_username import AccountUsernameAlreadyExists
from src.auth.account.infra.api.signup.signup_account_controller import SignupAccountController
from src.shared.domain.exceptions.base_error import BaseError
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.domain.mothers.account_username_primitives_mother import AccountUsernamePrimitivesMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestSignupController:
    _response = None
    _ANY_REQUEST_BODY = SignupAccountRequest(
        username=AccountUsernamePrimitivesMother.any(),
        email=AccountEmailPrimitivesMother.any(),
        password=AccountPasswordHashPrimitivesMother.any(),
    )
    _ANY_ACCOUNT_ID = AccountIdPrimitivesMother.any()

    def setup_method(self) -> None:
        self._use_case = AsyncMock(spec=AccountSignup)
        self._controller = SignupAccountController(use_case=self._use_case)

    async def test_should_return_202_when_signing_up_an_account_and_a_user_successfully(self) -> None:
        self._should_signup_account_and_user()

        self._response = await self._controller.signup(account_id=self._ANY_ACCOUNT_ID, **self._ANY_REQUEST_BODY.model_dump())

        self._assert_contract_is_met_on_success(202, {"accepted": True})

    @pytest.mark.parametrize(
        "expected_error",
        [
            pytest.param(AccountUsernameAlreadyExists, id="username"),
            pytest.param(AccountEmailAlreadyExists, id="email"),
        ],
    )
    async def test_should_return_409_when_signing_up_an_account_with_existing(
        self, expected_error: type[BaseError]
    ) -> None:
        self._should_fail_validating_signup_data_with(expected_error)

        self._response = await self._controller.signup(account_id=self._ANY_ACCOUNT_ID, **self._ANY_REQUEST_BODY.model_dump())

        self._assert_contract_is_met_on_error(409)

    def _should_signup_account_and_user(self) -> None:
        self._use_case.execute.return_value = None

    def _assert_contract_is_met_on_success(self, expected_status_code: int, expected_body: dict[str, bool]) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.data).to(equal(expected_body))

    def _should_fail_validating_signup_data_with(self, error: type[BaseError]) -> None:
        self._use_case.execute.side_effect = error

    def _assert_contract_is_met_on_error(self, expected_status_code: int) -> None:
        expect(self._response.status).to(equal(expected_status_code))
