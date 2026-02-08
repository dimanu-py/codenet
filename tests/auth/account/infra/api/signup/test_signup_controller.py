from unittest.mock import AsyncMock

import pytest
from expects import equal, expect

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup, EmailAlreadyExists
from src.auth.account.delivery.signup.signup_request import SignupRequest
from src.auth.account.infra.api.signup.signup_controller import SignupController
from src.backoffice.user.application.signup.user_signup import UsernameAlreadyExists
from src.shared.domain.exceptions.base_error import BaseError
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import AccountPasswordHashPrimitivesMother
from tests.backoffice.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestSignupController:
    _response = None

    def setup_method(self) -> None:
        self._use_case = AsyncMock(spec=AccountWithUserSignup)
        self._controller = SignupController(use_case=self._use_case)

    async def test_should_return_202_when_signing_up_an_account_and_a_user_successfully(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=AccountPasswordHashPrimitivesMother.any(),
        )
        account_id = AccountIdPrimitivesMother.any()
        self._should_signup_account_and_user()

        self._response = await self._controller.signup(account_id=account_id, **request_body.model_dump())

        self._assert_contract_is_met_on_success(202, {"accepted": True})

    async def test_should_return_409_when_signing_up_an_account_with_existing_username(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=AccountPasswordHashPrimitivesMother.any(),
        )
        account_id = AccountIdPrimitivesMother.any()
        self._should_fail_validating_signup_data_with(UsernameAlreadyExists)

        self._response = await self._controller.signup(account_id=account_id, **request_body.model_dump())

        self._assert_contract_is_met_on_error(409)

    async def test_should_return_409_when_signing_up_an_account_with_existing_email(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=AccountEmailPrimitivesMother.any(),
            password=AccountPasswordHashPrimitivesMother.any(),
        )
        account_id = AccountIdPrimitivesMother.any()
        self._should_fail_validating_signup_data_with(EmailAlreadyExists)

        self._response = await self._controller.signup(account_id=account_id, **request_body.model_dump())

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
