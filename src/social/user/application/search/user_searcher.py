from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository


class UserSearcher:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, filters: dict) -> list[User]:
        criteria = Criteria.from_primitives(filters)
        return await self._search_users_matching(criteria)

    async def _search_users_matching(self, criteria: Criteria) -> list[User]:
        return await self._repository.matching(criteria)
