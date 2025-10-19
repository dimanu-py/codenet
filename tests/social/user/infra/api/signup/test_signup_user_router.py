import json

import pytest
from doublex import ANY_ARG, when
from expects import equal, expect

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
    async def test_should_return_201_when_signup_data_is_valid(self) -> None:
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

    async def test_should_return_422_when_user_name_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name="Invalid@Name",
            username=UserUsernameMother.any().value,
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).raises(InvalidNameFormatError)

        response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=user_signup,
        )

        expect(response.status_code).to(equal(422))
        expect(json.loads(response.body)).to((equal({"detail": "Name cannot contain special characters or numbers."})))

    async def test_should_return_422_when_user_username_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username="Invalid*Username",
            email=UserEmailMother.any().value,
        )
        user_id = UserIdMother.any().value
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).raises(InvalidUsernameFormatError)

        response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=user_signup,
        )

        expect(response.status_code).to(equal(422))
        expect(json.loads(response.body)).to((equal({"detail": "Username cannot contain special characters"})))

    async def test_should_return_422_when_email_does_not_have_valid_format(self) -> None:
        request_body = UserSignupRequest(
            name=UserNameMother.any().value,
            username=UserUsernameMother.any().value,
            email="invalid-email-format",
        )
        user_id = UserIdMother.any().value
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).raises(InvalidEmailFormatError)

        response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=user_signup,
        )

        expect(response.status_code).to(equal(422))
        expect(json.loads(response.body)).to((equal({"detail": "Email cannot contain special characters and must contain '@' and '.'"})))
