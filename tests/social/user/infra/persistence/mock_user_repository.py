from unittest.mock import AsyncMock

from expects import expect, equal

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_repository import UserRepository


class MockUserRepository(UserRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()
        self._mock_match = AsyncMock()

    async def save(self, user: User) -> None:
        self._mock_save(user)

    async def search(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    async def matching(self, criteria: Criteria) -> list[User] | None:
        return self._mock_match(criteria)  # type: ignore

    def should_save(self, user: User) -> None:
        def verify(expected_user: User) -> None:
            expect(user).to(equal(expected_user))

        self._mock_save = verify  # type: ignore

    def should_match(self, criteria: Criteria, users: list[User]) -> None:
        def verify(expected_criteria: Criteria) -> list[User]:
            expect(criteria).to(equal(expected_criteria))
            return users

        self._mock_match = verify  # type: ignore

    def should_not_match(self, criteria):
        def verify(expected_criteria: Criteria) -> list:
            expect(criteria).to(equal(expected_criteria))
            return []

        self._mock_match = verify  # type: ignore
