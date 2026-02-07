from src.shared.infra.http.success_response import OkResponse, SuccessResponse
from src.backoffice.user.application.search.user_searcher import UserSearcher


class UserSearchController:
    def __init__(self, use_case: UserSearcher) -> None:
        self._searcher = use_case

    async def search(self, filters: dict) -> SuccessResponse:
        users = await self._searcher.execute(filters)

        return OkResponse(data=[user.to_primitives() for user in users])
