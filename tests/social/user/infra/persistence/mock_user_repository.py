from unittest.mock import AsyncMock

from expects import expect, equal

from src.social.user.domain.user import User
from src.social.user.domain.user_repository import UserRepository


class MockUserRepository(UserRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()

    async def save(self, user: User) -> None:
        self._mock_save(user)

    def should_save(self, user: User) -> None:
        def verify(expected_user: User) -> None:
            expect(user).to(equal(expected_user))

        self._mock_save = verify  # type: ignore
