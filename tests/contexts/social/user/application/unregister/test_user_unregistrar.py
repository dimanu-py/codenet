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
from src.contexts.social.user.domain.user_id import UserId
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

    def setup_method(self) -> None:
        self._repository = Mock(UserRepository)
        self._user_unregistrar = UserUnregistrar(repository=self._repository)

    @pytest.mark.asyncio
    async def test_should_unregister_an_existing_user(self) -> None:
        user_id = UserIdMother.create()
        self.should_search_user(user_id)
        self.should_delete_user(user_id)

        await self._user_unregistrar(user_id.value)

        self.assert_has_satisfied_conditions()

    def assert_has_satisfied_conditions(self) -> None:
        expect(self._repository).to(have_been_satisfied)

    def should_delete_user(self, user_id: UserId) -> None:
        expect_call(self._repository).delete(user_id).returns(self._immediate_future())

    def should_search_user(self, user_id: UserId) -> None:
        expect_call(self._repository).search(user_id).returns(
            self._immediate_future(user_id)
        )

    @pytest.mark.asyncio
    async def test_should_not_allow_to_unregister_no_existing_user(self) -> None:
        user_id = UserIdMother.create()
        self.should_search_and_return_none(user_id)

        await async_expect(lambda: self._user_unregistrar(user_id.value)).to(
            raise_error(UserDoesNotExistError)
        )

    def should_search_and_return_none(self, user_id: UserId) -> None:
        expect_call(self._repository).search(user_id).returns(self._immediate_future())
