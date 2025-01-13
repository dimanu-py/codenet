from asyncio import Future

import pytest
from doublex import Mock, expect_call
from doublex_expects import have_been_satisfied
from expects import expect

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_id import UserId
from src.contexts.social.user.domain.user_repository import UserRepository


@pytest.mark.unit
class UserModuleUnitTestConfig:
    _repository = Mock(UserRepository)

    def should_save_user(self, user: User) -> None:
        expect_call(self._repository).save(user).returns(self._immediate_future())

    def should_delete_user(self, user_id: UserId) -> None:
        expect_call(self._repository).delete(user_id).returns(self._immediate_future())

    def should_search_user(self, user_id: UserId) -> None:
        expect_call(self._repository).search(user_id).returns(
            self._immediate_future(user_id)
        )

    def should_search_and_return_none(self, user_id: UserId) -> None:
        expect_call(self._repository).search(user_id).returns(self._immediate_future())

    def assert_has_satisfied_conditions(self):
        expect(self._repository).to(have_been_satisfied)

    @staticmethod
    def _immediate_future(result=None) -> Future:
        future: Future = Future()
        future.set_result(result)
        return future
