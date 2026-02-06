from src.social.user.application.removal.user_not_found import UserNotFound
from src.social.user.application.removal.user_remover import UserRemover
from tests.shared.expects.matchers import async_expect, raise_error
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.mothers.user_mother import UserMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


class TestUserRemover(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_remover = UserRemover(repository=self._repository)

    async def test_should_remove_existing_user_based_on_username(self) -> None:
        username = UserUsernamePrimitivesMother.any()
        user = UserMother.with_username(username)
        self._should_search_and_find(user)

        await self._user_remover.execute(username)

        self._should_have_removed(user)

    async def test_should_not_allow_to_remove_non_signup_user(self) -> None:
        username = UserUsernamePrimitivesMother.any()

        self._should_search_and_not_find_user()

        await async_expect(lambda: self._user_remover.execute(username)).to(raise_error(UserNotFound))
