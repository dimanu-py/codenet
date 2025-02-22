import pytest

from src.shared.domain.exceptions.invalid_id_format_error import InvalidIdFormatError
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.domain.invalid_email_format_error import InvalidEmailFormatError
from src.social.user.domain.invalid_name_format_error import InvalidNameFormatError
from src.social.user.domain.invalid_username_format_error import (
    InvalidUsernameFormatError,
)
from tests.social.shared.expects.matchers import async_expect, raise_error
from tests.social.user.application.signup.user_signup_command_mother import (
    UserSignupCommandMother,
)
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.user_mother import UserMother


class TestUserSignup(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_signup = UserSignup(repository=self._repository)

    async def test_should_signup_user(self) -> None:
        command = UserSignupCommandMother.any()
        user = UserMother.create(command.to_dict())

        self._should_save(user)

        await self._user_signup(command)

    @pytest.mark.parametrize(
        "invalid_field, expected_error",
        [
            ({"id": "12345"}, InvalidIdFormatError),
            ({"name": "John!"}, InvalidNameFormatError),
            ({"username": "john#doe"}, InvalidUsernameFormatError),
            ({"email": "john.doe_hotmail.com"}, InvalidEmailFormatError),
        ],
    )
    async def test_should_not_allow_to_signup_invalid_user(
        self, invalid_field: dict[str, str], expected_error: Exception
    ) -> None:
        command = UserSignupCommandMother.invalid(invalid_field)

        await async_expect(lambda: self._user_signup(command)).to(
            raise_error(expected_error)
        )
