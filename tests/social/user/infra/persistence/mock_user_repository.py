from unittest.mock import AsyncMock

from expects import equal, expect

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository
from src.social.user.domain.user_username import UserUsername


class MockUserRepository(UserRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()
        self._mock_match = AsyncMock()
        self._mock_find = AsyncMock()
        self._mock_remove = AsyncMock()

    async def save(self, user: User) -> None:
        self._mock_save(user)

    async def search(self, username: UserId) -> User | None:
        return self._mock_find(username)  # type: ignore

    async def matching(self, criteria: Criteria) -> list[User]:
        return self._mock_match(criteria)  # type: ignore

    async def delete(self, username: UserId) -> None:
        return self._mock_remove(username)  # type: ignore

    def should_save(self, user: User) -> None:
        def verify(expected_user: User) -> None:
            expect(user.to_public_primitives()).to(equal(expected_user.to_public_primitives()))

        self._mock_save = verify  # type: ignore

    def should_match(self, criteria: Criteria, users: list[User]) -> None:
        def verify(expected_criteria: Criteria) -> list[User]:
            expect(criteria).to(equal(expected_criteria))
            return users

        self._mock_match = verify  # type: ignore

    def should_not_match(self, criteria: Criteria) -> None:
        def verify(expected_criteria: Criteria) -> list:
            expect(criteria).to(equal(expected_criteria))
            return []

        self._mock_match = verify  # type: ignore

    def should_find(self, user: User) -> None:
        def verify(expected_user_username: UserUsername) -> User:
            expect(user.username).to(equal(expected_user_username))
            return user

        self._mock_find = verify  # type: ignore

    def should_remove(self, user: User) -> None:
        def verify(expected_user_username: UserUsername) -> None:
            expect(user.username).to(equal(expected_user_username))

        self._mock_remove = verify  # type: ignore

    def should_not_find(self, user_username: UserUsername) -> None:
        def verify(expected_user_username: UserUsername) -> None:
            expect(user_username).to(equal(expected_user_username))
            return None

        self._mock_find = verify  # type: ignore
