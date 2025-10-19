import json

import pytest
from doublex import ANY_ARG, when
from expects import equal, expect

from src.shared.domain.exceptions.domain_error import DomainError
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.domain.user_email import InvalidEmailFormatError
from src.social.user.domain.user_name import InvalidNameFormatError
from src.social.user.domain.user_username import InvalidUsernameFormatError
from src.social.user.infra.api.signup.signup_user_router import signup_user
from src.social.user.infra.api.signup.user_sign_up_request import UserSignupRequest
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_email_mother import UserEmailMother
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.domain.mothers.user_name_mother import UserNameMother
from tests.social.user.domain.mothers.user_username_mother import UserUsernameMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestSignupUserRouter:
    def setup_method(self) -> None:
        self._user_signup = AsyncStub(UserSignup)
        self._response = None

    async def test_should_return_201_when_signup_data_is_valid(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        self._stub_successful_signup()

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(201, {f"resource": f"/app/users/{user_id}"})

    async def test_should_return_422_when_user_name_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name="Invalid@Name",
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        self._stub_signup_error(InvalidNameFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(422, {"detail": "Name cannot contain special characters or numbers."})

    async def test_should_return_422_when_user_username_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username="Invalid*Username",
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        self._stub_signup_error(InvalidUsernameFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(422, {"detail": "Username cannot contain special characters"})

    async def test_should_return_422_when_email_does_not_have_valid_format(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email="invalid-email-format",
        )
        user_id = UserIdMother.any().value
        self._stub_signup_error(InvalidEmailFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(
            422, {"detail": "Email cannot contain special characters and must contain '@' and '.'"}
        )

    def _stub_successful_signup(self) -> None:
        when(self._user_signup).execute(ANY_ARG).returns(None)

    def _stub_signup_error(self, error: DomainError) -> None:
        when(self._user_signup).execute(ANY_ARG).raises(error)

    def _assert_contract_is_met_with(self, expected_status_code: int, expected_body: dict) -> None:
        expect(self._response.status_code).to(equal(expected_status_code))
        expect(json.loads(self._response.body)).to(equal(expected_body))
