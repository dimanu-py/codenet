from unittest.mock import AsyncMock

from src.backoffice.user.application.search.user_searcher import UserSearcher
from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.api.search.user_search_controller import UserSearchController
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.backoffice.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother


class TestUserSearchController(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._use_case = AsyncMock(spec=UserSearcher)
        self._controller = UserSearchController(use_case=self._use_case)

    async def test_should_return_200_when_users_are_found_and_response_contains_list_of_users(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        user = UserMother.any()
        self._should_find_user(user)

        self._response = await self._controller.search(filters=filters)

        self._assert_contract_is_met_on_success(200, [user.to_primitives()])

    async def test_should_return_200_when_users_are_not_found_and_response_is_an_empty_list(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        self._should_not_find_user()

        self._response = await self._controller.search(filters=filters)

        self._assert_contract_is_met_on_success(200, [])

    def _should_not_find_user(self) -> None:
        self._use_case.execute.return_value = []

    def _should_find_user(self, user: User) -> None:
        self._use_case.execute.return_value = [user]
