from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect

from src.contexts.shared.domain.exceptions.invalid_id_format_error import (
    InvalidIdFormatError,
)
from src.contexts.social.user.application.register.user_registrar import UserRegistrar
from src.contexts.social.user.domain.invalid_email_format_error import (
    InvalidEmailFormatError,
)
from src.contexts.social.user.domain.invalid_name_format_error import (
    InvalidNameFormatError,
)
from src.contexts.social.user.domain.invalid_url_format_error import (
    InvalidUrlFormatError,
)
from src.contexts.social.user.domain.invalid_username_format_error import (
    InvalidUsernameFormatError,
)
from src.contexts.social.user.domain.user_repository import UserRepository
from tests.contexts.shared.expects.matchers import async_expect, raise_error
from tests.contexts.social.user.application.register.register_user_command_mother import (
    RegisterUserCommandMother,
)
from tests.contexts.social.user.domain.user_mother import UserMother


@pytest.mark.unit
class TestUserRegistrar:
    @staticmethod
    def _immediate_future(result=None) -> Future:
        future: Future = Future()
        future.set_result(result)
        return future

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        command = RegisterUserCommandMother.create()
        user = UserMother.from_command(command)
        repository = Mock(UserRepository)
        user_registrar = UserRegistrar(repository=repository)
        expect_call(repository).save(user).returns(self._immediate_future())

        await user_registrar(command)

        expect(repository).to(have_been_satisfied)

    @pytest.mark.parametrize(
        "invalid_field, expected_error",
        [
            ({"id": "12345"}, InvalidIdFormatError),
            ({"name": "John!"}, InvalidNameFormatError),
            ({"username": "@john#doe"}, InvalidUsernameFormatError),
            ({"email": "johndoe.com"}, InvalidEmailFormatError),
            ({"profile_picture": "picture.jpg"}, InvalidUrlFormatError),
        ],
    )
    @pytest.mark.asyncio
    async def test_should_not_allow_to_store_an_invalid_user(
        self, invalid_field: dict, expected_error: Exception
    ) -> None:
        repository = Mock(UserRepository)
        user_registrar = UserRegistrar(repository=repository)
        command = RegisterUserCommandMother.create(invalid_field)

        await async_expect(lambda: user_registrar(command)).to(
            raise_error(expected_error)
        )
