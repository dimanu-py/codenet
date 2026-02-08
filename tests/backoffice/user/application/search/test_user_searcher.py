from expects import be_empty, equal, expect

from src.backoffice.user.application.search.user_searcher import UserSearcher
from tests.backoffice.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother


class TestUserSearcher(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_searcher = UserSearcher(repository=self._repository)

    async def test_should_search_existing_user(self) -> None:
        criteria = CriteriaMother.any()
        users = [UserMother.any()]
        self._should_match_criteria_with(users)

        found_users = await self._user_searcher.execute(criteria.to_primitives())

        expect(found_users).to(equal(users))

    async def test_should_return_empty_list_when_no_user_matches_criteria(self) -> None:
        criteria = CriteriaMother.any()
        self._should_not_match_criteria()

        found_users = await self._user_searcher.execute(criteria.to_primitives())

        expect(found_users).to(be_empty)
