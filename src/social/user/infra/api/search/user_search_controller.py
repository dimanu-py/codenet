from src.shared.infra.http.success_response import OkResponse, SuccessResponse
from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.application.search.user_search_response import UserSearchResponse
from src.social.user.application.search.user_searcher import UserSearcher


class UserSearchController:
    def __init__(self, use_case: UserSearcher) -> None:
        self._searcher = use_case

    async def search(self, filters: dict) -> SuccessResponse:
        query = SearchUserQuery(filters=filters)

        users = await self._searcher.execute(query)

        response = UserSearchResponse([user.to_public_primitives() for user in users])

        return OkResponse(data=[user.to_public_primitives() for user in users])
