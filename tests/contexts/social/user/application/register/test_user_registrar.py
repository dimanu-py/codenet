from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect

from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.application.register.user_registrar import UserRegistrar
from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_repository import UserRepository


@pytest.mark.unit
class TestUserRegistrar:
    @staticmethod
    def _immediate_future(result=None) -> Future:
        future: Future = Future()
        future.set_result(result)
        return future

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        repository = Mock(UserRepository)
        user_registrar = UserRegistrar(repository=repository)
        user = User(
            id_="897585f-4d7a-42ba-8d82-ab8da94d2c4a",
            name="John Doe",
            username="john_doe",
            email="johndoe@gmail.com",
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )
        expect_call(repository).save(user).returns(self._immediate_future())
        command = RegisterUserCommand(
            id=user._id,
            name=user._name,
            username=user._username,
            email=user._email,
            profile_picture=user._profile_picture,
        )

        await user_registrar(command)

        expect(repository).to(have_been_satisfied)
