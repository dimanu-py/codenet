from expects import expect, equal, be_empty

from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_searcher import UserSearcher
from tests.shared.domain.criteria.criteria_mother import CriteriaMother
from tests.social.user.application.user_module_unit_test_config import (
    UserModuleUnitTestConfig,
)
from tests.social.user.domain.mother.user_mother import UserMother


class TestUserSearcher(UserModuleUnitTestConfig):
    def setup_method(self) -> None:
        self._user_searcher = UserSearcher(repository=self._repository)

    async def test_should_search_existing_user(self) -> None:
        criteria = CriteriaMother.any()
        query = SearchUserQuery(criteria.to_primitives())
        users = [UserMother.any()]

        self._should_match(criteria, users)

        searched_users = await self._user_searcher(query)

        expect(searched_users).to(equal(users))

    async def test_should_return_empty_list_when_no_user_matches_criteria(self) -> None:
        criteria = CriteriaMother.any()
        query = SearchUserQuery(criteria.to_primitives())

        self._should_not_match(criteria)

        searched_users = await self._user_searcher(query)

        expect(searched_users).to(be_empty)
