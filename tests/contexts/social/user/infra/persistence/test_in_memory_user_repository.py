import pytest
from expects import expect, equal

from src.contexts.social.user.infra.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from tests.contexts.social.user.domain.user_mother import UserMother


@pytest.mark.integration
class TestInMemoryUserRepository:
    @pytest.mark.asyncio
    async def test_should_save_valid_user(self) -> None:
        repository = InMemoryUserRepository()
        user = UserMother.create()

        await repository.save(user)

        saved_user = await repository.search(user.id.value)
        expect(saved_user).to(equal(user))

    @pytest.mark.asyncio
    async def test_should_delete_valid_user(self) -> None:
        repository = InMemoryUserRepository()
        user = UserMother.create()
        await repository.save(user)

        await repository.delete(user.id.value)

        saved_user = await repository.search(user.id.value)
        expect(saved_user).to(equal(None))
