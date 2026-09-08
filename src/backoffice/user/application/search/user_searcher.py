from src.backoffice.user.domain.user import User
from src.backoffice.user.domain.user_repository import UserRepository
from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.criteria_converter import FiltersToCriteriaConverter


class UserSearcher:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, filters: dict, sorts: list[dict]) -> list[User]:
        criteria = FiltersToCriteriaConverter.convert(filters, sorts)
        return await self._search_users_matching(criteria)

    async def _search_users_matching(self, criteria: Criteria) -> list[User]:
        return await self._repository.matching(criteria)
