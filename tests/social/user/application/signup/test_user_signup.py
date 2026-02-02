from src.social.user.application.signup.user_signup import UserSignup
from tests.shared.expects.matchers import async_expect, raise_error
from tests.social.user.application.signup.user_signup_command_mother import (
    UserSignupCommandMother,
)
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.mothers.user_mother import UserMother
from tests.social.user.domain.user_already_exists import UsernameAlreadyExists


class TestUserSignup(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_signup = UserSignup(repository=self._repository)

    async def test_should_signup_user(self) -> None:
        command = UserSignupCommandMother.any()
        user = UserMother.from_signup_command(command)
        self._should_search_and_not_find(user)

        self._should_save(user)

        await self._user_signup.execute(command)

    async def test_should_not_allow_signup_user_with_existing_username(self) -> None:
        command = UserSignupCommandMother.any()
        existing_user = UserMother.from_signup_command(command)
        self._should_search_and_find(existing_user)

        await async_expect(lambda: self._user_signup.execute(command)).to(raise_error(UsernameAlreadyExists))
