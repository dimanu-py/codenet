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
        self._mock_remove = AsyncMock()

    async def save(self, user: User) -> None:
        self._mock_save.assert_called_once_with(user.to_public_primitives())

    async def search(self, username: UserUsername) -> User | None:
        self._mock_search.assert_called_once_with(username)
        return self._mock_search.return_value

    async def matching(self, criteria: Criteria) -> list[User]:
        self._mock_match.assert_called_once_with(criteria)
        return self._mock_match.return_value

    async def delete(self, username: UserUsername) -> None:
        self._mock_remove.assert_called_once_with(username)

    def should_save(self, user: User) -> None:
        self._mock_save(user.to_public_primitives())

    def should_match(self, criteria: Criteria, users: list[User]) -> None:
        self._mock_match(criteria)
        self._mock_match.return_value = users

    def should_not_match(self, criteria: Criteria) -> None:
        self._mock_match(criteria)
        self._mock_match.return_value = []

    def should_search(self, user: User) -> None:
        self._mock_search(user.username)
        self._mock_search.return_value = Optional.of(user)

    def should_not_search(self, user: User) -> None:
        self._mock_search(user.username)
        self._mock_search.return_value = Optional.empty()

    def should_remove(self, user: User) -> None:
        self._mock_remove(user.username)

    def reset_mocks(self) -> None:
        self._mock_save.reset_mock(return_value=True, side_effect=True)
        self._mock_match.reset_mock(return_value=True, side_effect=True)
        self._mock_search.reset_mock(return_value=True, side_effect=True)
        self._mock_remove.reset_mock(return_value=True, side_effect=True)
