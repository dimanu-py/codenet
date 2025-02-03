import pytest

from src.social.user.application.signup.user_signup import UserSignup
from src.shared.domain.exceptions.invalid_id_format_error import InvalidIdFormatError
from tests.social.shared.expects.matchers import async_expect, raise_error
from tests.social.user.application.signup.user_signup_command_mother import (
    UserSignupCommandMother,
)
from tests.social.user.domain.user_mother import UserMother
from tests.social.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
class TestUserSignup:
    @pytest.mark.asyncio
    async def test_should_signup_user(self) -> None:
        command = UserSignupCommandMother.any()
        user = UserMother.from_command(command)
        user_repository = MockUserRepository()
        user_signup = UserSignup(repository=user_repository)

        user_repository.should_save(user)

        await user_signup(command)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_field, expected_error",
        [({"id": "12345"}, InvalidIdFormatError)],
    )
    async def test_should_not_allow_to_signup_invalid_user(
        self, invalid_field: dict[str, str], expected_error: Exception
    ) -> None:
        command = UserSignupCommandMother.invalid(invalid_field)
        user_repository = MockUserRepository()
        user_signup = UserSignup(repository=user_repository)

        await async_expect(lambda: user_signup(command)).to(raise_error(expected_error))
