from doublex import ANY_ARG, when

from src.social.user.application.removal.user_not_found_error import UserNotFoundError
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.infra.api.removal.removal_user_router import remove_user
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig


class TestRemovalUserRouter(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._user_remover = AsyncStub(UserRemover)

    async def test_should_return_202_when_user_is_removed(self) -> None:
        user_id = UserIdMother.any().value
        self._should_remove_user()

        self._response = await remove_user(
            user_id=user_id,
            user_remover=self._user_remover,
        )

        self._assert_contract_is_met_with(202, {"message": "User removal request has been accepted."})

    async def test_should_return_404_when_user_to_remove_does_not_exist(self) -> None:
        user_id = UserIdMother.any().value
        self._should_not_find_user()

        self._response = await remove_user(
            user_id=user_id,
            user_remover=self._user_remover,
        )

        self._assert_contract_is_met_with(404, {"detail": "User with that id not found"})

    def _should_remove_user(self) -> None:
        when(self._user_remover).execute(ANY_ARG).returns(None)

    def _should_not_find_user(self) -> None:
        when(self._user_remover).execute(ANY_ARG).raises(UserNotFoundError)
