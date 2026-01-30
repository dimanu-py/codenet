from doublex import ANY_ARG, when

from src.social.user.application.removal.user_not_found import UserNotFound
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.infra.api.removal.user_removal_controller import UserRemovalController
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother
from tests.social.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig


class TestUserRemovalController(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._use_case = AsyncStub(UserRemover)
        self._controller = UserRemovalController(use_case=self._use_case)

    async def test_should_return_202_when_user_is_removed(self) -> None:
        user_username = UserUsernamePrimitivesMother.any()
        self._should_remove_user()

        self._response = await self._controller.remove(username=user_username)

        self._assert_contract_is_met_with(202, {"message": "User removal request has been accepted."})

    async def test_should_return_404_when_user_to_remove_does_not_exist(self) -> None:
        user_username = UserUsernamePrimitivesMother.any()
        self._should_not_find_user()

        self._response = await self._controller.remove(username=user_username)

        self._assert_contract_is_met_with(404, {"message": "User with that id not found"})

    def _should_remove_user(self) -> None:
        when(self._use_case).execute(ANY_ARG).returns(None)

    def _should_not_find_user(self) -> None:
        when(self._use_case).execute(ANY_ARG).raises(UserNotFound)
