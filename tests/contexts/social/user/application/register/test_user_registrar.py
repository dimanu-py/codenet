from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect

from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.application.register.user_registrar import UserRegistrar
from src.contexts.shared.domain.exceptions.invalid_id_format_error import (
    InvalidIdFormatError,
)
from src.contexts.social.user.domain.invalid_email_format_error import (
    InvalidEmailFormatError,
)
from src.contexts.social.user.domain.invalid_name_format_error import (
    InvalidNameFormatError,
)
from src.contexts.social.user.domain.invalid_username_format_error import (
    InvalidUsernameFormatError,
)
from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_email import UserEmail
from src.contexts.social.user.domain.user_full_name import UserFullName
from src.contexts.social.user.domain.user_id import UserId
from src.contexts.social.user.domain.user_name import UserName
from src.contexts.social.user.domain.user_repository import UserRepository
from tests.contexts.shared.expects.matchers import async_expect, raise_error


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
            id_=UserId("8a97585f-4d7a-42ba-8d82-ab8da94d2c4a"),
            name=UserFullName("John Doe"),
            username=UserName("john_doe"),
            email=UserEmail("johndoe@gmail.com"),
            profile_picture="https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        )
        expect_call(repository).save(user).returns(self._immediate_future())
        command = RegisterUserCommand(
            id=user._id.value,
            name=user._name.value,
            username=user._username.value,
            email=user._email.value,
            profile_picture=user._profile_picture,
        )

        await user_registrar(command)

        expect(repository).to(have_been_satisfied)

    @pytest.mark.parametrize(
        "updates, expected_error",
        [
            ({"id": "12345"}, InvalidIdFormatError),
            ({"name": "John!"}, InvalidNameFormatError),
            ({"username": "@john#doe"}, InvalidUsernameFormatError),
            ({"email": "johndoe.com"}, InvalidEmailFormatError),
        ],
    )
    @pytest.mark.asyncio
    async def test_should_not_allow_to_store_an_invalid_user(
        self, updates: dict, expected_error: Exception
    ) -> None:
        primitives = {
            "id": "8a97585f-4d7a-42ba-8d82-ab8da94d2c4a",
            "name": "John Doe",
            "username": "john_doe",
            "email": "johndoe@gmail.com",
            "profile_picture": "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
            **updates,
        }
        repository = Mock(UserRepository)
        user_registrar = UserRegistrar(repository=repository)
        command = RegisterUserCommand(**primitives)

        await async_expect(lambda: user_registrar(command)).to(
            raise_error(expected_error)
        )
