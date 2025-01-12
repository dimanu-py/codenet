import pytest
from expects import expect, equal

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.infra.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)


@pytest.mark.integration
class TestInMemoryUserRepository:
    def test_should_save_valid_user(self) -> None:
        repository = InMemoryUserRepository()
        user = User(
            id_="1f322ec7-a36c-44e2-b339-71b966f95a99",
            name="John Doe",
            username="john_doe",
            email="johndoe@gmail.com",
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )

        repository.save(user)

        saved_user = repository.search(user.id)
        expect(saved_user).to(equal(user))
