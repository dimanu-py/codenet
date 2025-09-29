from src.social.user.application.signup.user_signup import UserSignup
from tests.social.user.application.signup.user_signup_command_mother import (
    UserSignupCommandMother,
)
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.mothers.user_mother import UserMother


class TestUserSignup(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_signup = UserSignup(repository=self._repository)

    async def test_should_signup_user(self) -> None:
        command = UserSignupCommandMother.any()
        user = UserMother.from_signup_command(command)

        self._should_save(user)

        await self._user_signup(command)
