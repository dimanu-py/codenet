from unittest.mock import AsyncMock

from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.value_objects.optional import Optional
from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository
from src.social.user.domain.user_username import UserUsername


class MockUserRepository(UserRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()
        self._mock_match = AsyncMock()
        self._mock_search = AsyncMock()

    async def save(self, user: User) -> None:
        await self._mock_save(user.to_primitives())

    async def search(self, username: UserUsername) -> User | None:
        await self._mock_search(username)
        return self._mock_search.return_value

    async def matching(self, criteria: Criteria) -> list[User]:
        await self._mock_match(criteria)
        return self._mock_match.return_value

    async def delete(self, username: UserUsername) -> None:
        await self._mock_save(username)

    def should_have_saved(self, user: User) -> None:
        self._mock_save.assert_awaited_once_with(user.to_primitives())

    def should_match_criteria_with(self, users: list[User]) -> None:
        self._mock_match.return_value = users

    def should_not_match_criteria(self) -> None:
        self._mock_match.return_value = []

    def should_search(self, user: User) -> None:
        self._mock_search.return_value = Optional.of(user)

    def should_not_search_user(self) -> None:
        self._mock_search.return_value = Optional.empty()

    def should_have_removed(self, user: User) -> None:
        self._mock_save.assert_awaited_once_with(user.username)

    def reset_mocks(self) -> None:
        self._mock_save.reset_mock(return_value=True, side_effect=True)
        self._mock_match.reset_mock(return_value=True, side_effect=True)
        self._mock_search.reset_mock(return_value=True, side_effect=True)
