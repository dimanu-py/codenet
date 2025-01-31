import pytest

from src.social.user.infra.in_memory_user_repository import InMemoryUserRepository
from tests.social.user.domain.user_mother import UserMother


@pytest.mark.integration
class TestInMemoryUserRepository:
    @pytest.mark.asyncio
    async def test_should_signup_a_user(self) -> None:
        user = UserMother.any()
        user_repository = InMemoryUserRepository()

        await user_repository.save(user)
