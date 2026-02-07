from unittest.mock import AsyncMock

import pytest
from expects import equal, expect

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.auth.account.delivery.signup.signup_request import SignupRequest
from src.auth.account.infra.api.signup.signup_controller import SignupController
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import UserPasswordPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


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
            password=UserPasswordPrimitivesMother.any(),
        )
        account_id = AccountIdPrimitivesMother.any()
        self._should_signup_account_and_user()

        self._response = await self._controller.signup(account_id=account_id, **request_body.model_dump())

        self._assert_contract_is_met_on_success(202, {"accepted": True})

    def _should_signup_account_and_user(self) -> None:
        self._use_case.execute.return_value = None

    def _assert_contract_is_met_on_success(self, expected_status_code: int, expected_body: dict[str, bool]) -> None:
        expect(self._response.status).to(equal(expected_status_code))
        expect(self._response.data).to(equal(expected_body))
