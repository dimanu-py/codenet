from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect

from src.contexts.social.user.application.unregister.user_unregistrar import (
    UserUnregistrar,
)
from src.contexts.social.user.domain.user_repository import UserRepository


@pytest.mark.unit
class TestUserUnregistrar:
    @staticmethod
    def _immediate_future(result=None) -> Future:
        future: Future = Future()
        future.set_result(result)
        return future

    @pytest.mark.asyncio
    async def test_should_unregister_an_existing_user(self) -> None:
        repository = Mock(UserRepository)
        user_unregistrar = UserUnregistrar(repository=repository)
        user_id = "2827970-f484-48a2-abd2-aa8f205b295a"
        expect_call(repository).delete(user_id).returns(self._immediate_future())

        await user_unregistrar(user_id)

        expect(repository).to(have_been_satisfied)