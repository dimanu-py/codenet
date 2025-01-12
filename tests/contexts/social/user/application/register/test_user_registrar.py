import pytest
from expects import expect
from doublex import Spy
from doublex_expects import have_been_called_with

from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.application.register.user_registrar import UserRegistrar
from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_repository import UserRepository


@pytest.mark.unit
class TestUserRegistrar:
    @pytest.mark.xfail
    def test_should_register_a_valid_user(self) -> None:
        repository = Spy(UserRepository)
        user_registrar = UserRegistrar(repository=repository)
        user = User(
            id_="897585f-4d7a-42ba-8d82-ab8da94d2c4a",
            name="John Doe",
            username="john_doe",
            email="johndoe@gmail.com",
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )
        command = RegisterUserCommand(
            id=user._id,
            name=user._name,
            username=user._username,
            email=user._email,
            profile_picture=user._profile_picture,
        )

        user_registrar(command)

        expect(repository.save).to(have_been_called_with(user))
