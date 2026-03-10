from src.backoffice.user.application.search.user_searcher import UserSearcher
from src.shared.domain.criteria.invalid_criteria import InvalidCriteria
from src.shared.infra.api.error_response import BadRequestError, ErrorResponse
from src.shared.infra.api.success_response import OkResponse, SuccessResponse


class UserSearchController:
    def __init__(self, use_case: UserSearcher) -> None:
        self._searcher = use_case

    async def search(self, filters: dict, sorts: list[dict]) -> SuccessResponse | ErrorResponse:
        try:
            users = await self._searcher.execute(filters, sorts)
        except InvalidCriteria as error:
            return BadRequestError(error=error.to_primitives())

        return OkResponse(data=[user.to_primitives() for user in users])
