import json

import pytest
from doublex import ANY_ARG, when
from expects import equal, expect

from src.shared.domain.exceptions.domain_error import DomainError
from src.social.user.application.signup.user_signup import UserSignup
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
    async def test_should_receive_successful_response_when_sending_valid_signup_data(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).returns(None)

        response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=user_signup,
        )

        expect(response.status_code).to(equal(201))
        expect(json.loads(response.body)).to(equal({"resource": f"/app/users/{user_id}"}))

    async def test_should_return_422_when_user_id_does_not_fulfill_uuid_format(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )
        invalid_user_id = "invalid-uuid-format"
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).raises(
            DomainError(message="User id must be a valid UUID", error_type="invalid_user_id")
        )

        response = await signup_user(
            request=request_body,
            user_id=invalid_user_id,
            user_signup=user_signup,
        )

        expect(response.status_code).to(equal(422))
        expect(json.loads(response.body)).to((
            equal({
                "detail": "User id must be a valid UUID"
            })
        ))
