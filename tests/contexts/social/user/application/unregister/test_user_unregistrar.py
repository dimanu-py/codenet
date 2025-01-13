import pytest

from src.contexts.social.user.application.unregister.user_unregistrar import (
    UserUnregistrar,
)
from src.contexts.social.user.domain.user_does_not_exist_error import (
    UserDoesNotExistError,
)
from tests.contexts.shared.expects.matchers import async_expect, raise_error
from tests.contexts.social.user.domain.user_id_mother import UserIdMother
from tests.contexts.social.user.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)


@pytest.mark.asyncio
class TestUserUnregistrar(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_unregistrar = UserUnregistrar(repository=self._repository)

    async def test_should_unregister_an_existing_user(self) -> None:
        user_id = UserIdMother.create()
        self.should_search_user(user_id)
        self.should_delete_user(user_id)

        await self._user_unregistrar(user_id.value)

        self.assert_has_satisfied_conditions()

    @pytest.mark.asyncio
    async def test_should_not_allow_to_unregister_no_existing_user(self) -> None:
        user_id = UserIdMother.create()
        self.should_search_and_return_none(user_id)

        await async_expect(lambda: self._user_unregistrar(user_id.value)).to(
            raise_error(UserDoesNotExistError)
        )
