from src.backoffice.user.application.signup.user_signup import UserSignup, UsernameAlreadyExists
from tests.backoffice.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.shared.expects.matchers import async_expect, raise_error


class TestUserSignup(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_signup = UserSignup(repository=self._repository)

    async def test_should_signup_user(self) -> None:
        user = UserMother.any()
        self._should_search_and_not_find_user()

        await self._user_signup.execute(**user.to_primitives())

        self._should_have_saved(user)

    async def test_should_not_allow_to_signup_a_user_with_existing_username(self) -> None:
        existing_user = UserMother.any()
        self._should_search_and_find(existing_user)

        await async_expect(lambda: self._user_signup.execute(**existing_user.to_primitives())).to(
            raise_error(UsernameAlreadyExists)
        )
