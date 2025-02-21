from src.shared.domain.criteria.criteria import Criteria
from src.social.user.application.search.search_user_query import SearchUserQuery
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository


class UserSearcher:
    _repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, query: SearchUserQuery) -> list[User] | None:
        criteria = Criteria.from_primitives(query.filters)
        searched_users = await self._repository.matching(criteria)
        return searched_users if searched_users else None
