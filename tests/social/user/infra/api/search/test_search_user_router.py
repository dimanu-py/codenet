import json

from doublex import when, ANY_ARG
from expects import expect, equal

from src.social.user.application.search.user_searcher import UserSearcher
from src.social.user.infra.api.search.search_user_router import get_user_by_criteria
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_mother import UserMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSearchUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_return_200_when_users_are_found_and_response_contains_list_of_users(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        user = UserMother.any()
        user_searcher = AsyncStub(UserSearcher)
        when(user_searcher).execute(
            ANY_ARG,
        ).returns([user])

        response = await get_user_by_criteria(
            filter=json.dumps(filters),
            user_searcher=user_searcher,
        )

        found_users = {"users": [user.to_primitives()]}
        expect(response.status_code).to(equal(200))
        expect(json.loads(response.body)).to(equal(found_users))

    async def test_should_return_200_when_users_are_not_found_and_response_is_an_empty_list(self) -> None:
        filters = CriteriaMother.any().to_primitives()
        user_searcher = AsyncStub(UserSearcher)
        when(user_searcher).execute(
            ANY_ARG,
        ).returns([])

        response = await get_user_by_criteria(
            filter=json.dumps(filters),
            user_searcher=user_searcher,
        )

        found_users = {"users": []}
        expect(response.status_code).to(equal(200))
        expect(json.loads(response.body)).to(equal(found_users))
