import pytest
from expects import expect, equal

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_full_name import UserFullName
from src.contexts.social.user.domain.user_id import UserId
from src.contexts.social.user.domain.user_name import UserName
from src.contexts.social.user.infra.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)


@pytest.mark.integration
class TestInMemoryUserRepository:
    @pytest.mark.asyncio
    async def test_should_save_valid_user(self) -> None:
        repository = InMemoryUserRepository()
        user = User(
            id_=UserId("1f322ec7-a36c-44e2-b339-71b966f95a99"),
            name=UserFullName("John Doe"),
            username=UserName("john_doe"),
            email="johndoe@gmail.com",
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )

        await repository.save(user)

        saved_user = await repository.search(user.id.value)
        expect(saved_user).to(equal(user))

    @pytest.mark.asyncio
    async def test_should_delete_valid_user(self) -> None:
        repository = InMemoryUserRepository()
        user = User(
            id_=UserId("1f322ec7-a36c-44e2-b339-71b966f95a99"),
            name=UserFullName("John Doe"),
            username=UserName("john_doe"),
            email="johndoe@gmail.com",
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )
        await repository.save(user)

        await repository.delete(user.id.value)

        saved_user = await repository.search(user.id.value)
        expect(saved_user).to(equal(None))
