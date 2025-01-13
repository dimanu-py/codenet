import pytest
from expects import expect, equal

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.infra.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from tests.contexts.social.user.domain.user_mother import UserMother


@pytest.mark.integration
class TestInMemoryUserRepository:
    def setup_method(self) -> None:
        self._repository = InMemoryUserRepository()

    @pytest.mark.asyncio
    async def test_should_save_valid_user(self) -> None:
        user = UserMother.create()

        await self._repository.save(user)

        saved_user = await self._repository.search(user.id)
        self.assert_users_match(saved_user, user)

    @pytest.mark.asyncio
    async def test_should_delete_valid_user(self) -> None:
        user = UserMother.create()
        await self._repository.save(user)

        await self._repository.delete(user.id)

        saved_user = await self._repository.search(user.id)
        self.assert_has_not_found(saved_user)

    def assert_users_match(self, expected_user: User | None, user: User | None) -> None:
        expect(expected_user).to(equal(user))

    def assert_has_not_found(self, user: User | None) -> None:
        expect(user).to(equal(None))
