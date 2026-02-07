import pytest

from src.backoffice.user.domain.user import User
from tests.backoffice.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
@pytest.mark.asyncio
class UserModuleUnitTestConfig:
    _repository = MockUserRepository()

    def teardown_method(self) -> None:
        self._repository.reset_mocks()

    def _should_have_saved(self, user: User) -> None:
        self._repository.should_have_saved(user)

    def _should_match_criteria_with(self, users: list[User]) -> None:
        self._repository.should_match_criteria_with(users)

    def _should_not_match_criteria(self) -> None:
        self._repository.should_not_match_criteria()

    def _should_search_and_find(self, user: User) -> None:
        self._repository.should_search(user)

    def _should_search_and_not_find_user(self) -> None:
        self._repository.should_not_search_user()

    def _should_have_removed(self, user: User) -> None:
        self._repository.should_have_removed(user)
