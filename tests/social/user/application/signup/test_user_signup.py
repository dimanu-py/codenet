import pytest

from src.social.user.application.signup.user_signup import UserSignup
from tests.social.user.domain.user_mother import UserMother
from tests.social.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
class TestUserSignup:
    @pytest.mark.asyncio
    async def test_should_signup_user(self) -> None:
        user = UserMother.any()
        user_repository = MockUserRepository()
        user_signup = UserSignup(repository=user_repository)

        user_repository.should_save(user)

        await user_signup(
            id_=user.id_,
            name=user.name,
            username=user.username,
            email=user.email,
        )
