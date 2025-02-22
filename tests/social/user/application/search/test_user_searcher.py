import pytest
from expects import expect, equal, be_empty

from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_searcher import UserSearcher
from tests.social.shared.domain.criteria.criteria_mother import CriteriaMother
from tests.social.user.domain.user_mother import UserMother
from tests.social.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
class TestUserSearcher:
    @pytest.mark.asyncio
    async def test_should_search_existing_user(self) -> None:
        criteria = CriteriaMother.any()
        query = SearchUserQuery(criteria.to_primitives())
        repository = MockUserRepository()
        user_searcher = UserSearcher(repository=repository)
        users = [UserMother.any()]

        repository.should_match(criteria, users)

        searched_users = await user_searcher(query)

        expect(searched_users).to(equal(users))

    @pytest.mark.asyncio
    async def test_should_return_empty_list_when_no_user_matches_criteria(self) -> None:
        criteria = CriteriaMother.any()
        query = SearchUserQuery(criteria.to_primitives())
        repository = MockUserRepository()
        user_searcher = UserSearcher(repository=repository)

        repository.should_not_match(criteria)

        searched_users = await user_searcher(query)

        expect(searched_users).to(be_empty)
