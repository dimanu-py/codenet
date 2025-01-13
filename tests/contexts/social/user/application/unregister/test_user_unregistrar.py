from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect
from src.contexts.social.user.application.unregister.user_unregistrar import (
    UserUnregistrar,
)
from src.contexts.social.user.domain.user_does_not_exist_error import (
    UserDoesNotExistError,
)
from src.contexts.social.user.domain.user_repository import UserRepository
from tests.contexts.shared.expects.matchers import async_expect, raise_error
from tests.contexts.social.user.domain.user_id_mother import UserIdMother


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
        user_id = UserIdMother.create()
        expect_call(repository).search(user_id).returns(self._immediate_future(user_id))
        expect_call(repository).delete(user_id).returns(self._immediate_future())

        await user_unregistrar(user_id.value)

        expect(repository).to(have_been_satisfied)

    @pytest.mark.asyncio
    async def test_should_not_allow_to_unregister_no_existing_user(self) -> None:
        repository = Mock(UserRepository)
        user_unregistrar = UserUnregistrar(repository=repository)
        user_id = UserIdMother.create()
        expect_call(repository).search(user_id).returns(self._immediate_future())

        await async_expect(lambda: user_unregistrar(user_id.value)).to(
            raise_error(UserDoesNotExistError)
        )
