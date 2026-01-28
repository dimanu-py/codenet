from doublex import ANY_ARG, when

from src.social.user.application.search.user_searcher import UserSearcher
from src.social.user.domain.user import User
from src.social.user.infra.api.search.user_search_controller import UserSearchController
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_mother import UserMother
from tests.social.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig


class TestUserSearchController(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._controller = UserSearchController(use_case=AsyncStub(UserSearcher))

    async def test_should_return_200_when_users_are_found_and_response_contains_list_of_users(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        user = UserMother.any()
        self._should_find_user(user)

        self._response = await self._controller.search(filters=filters)

        self._assert_contract_is_met_with(200, {"detail": {"users": [user.to_public_primitives()]}})

    async def test_should_return_200_when_users_are_not_found_and_response_is_an_empty_list(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        self._should_not_find_user()

        self._response = await self._controller.search(filters=filters)

        self._assert_contract_is_met_with(200, {"detail": {"users": []}})

    def _should_not_find_user(self) -> None:
        when(self._use_case).execute(
            ANY_ARG,
        ).returns([])

    def _should_find_user(self, user: User) -> None:
        when(self._use_case).execute(
            ANY_ARG,
        ).returns([user])
