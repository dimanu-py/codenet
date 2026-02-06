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
        user = UserMother.create(**command.to_primitives())
        self._should_search_and_not_find_user()

        await self._user_signup.execute(command)

        self._should_have_saved(user)

    async def test_should_not_allow_signup_user_with_existing_username(self) -> None:
        command = UserSignupCommandMother.any()
        existing_user = UserMother.create(**command.to_primitives())
        self._should_search_and_find(existing_user)

        await async_expect(lambda: self._user_signup.execute(command)).to(raise_error(UsernameAlreadyExists))
