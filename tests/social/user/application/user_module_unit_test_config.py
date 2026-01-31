import pytest

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from tests.social.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
@pytest.mark.asyncio
class UserModuleUnitTestConfig:
    _repository = MockUserRepository()

    def teardown_method(self) -> None:
        self._repository.reset_mocks()

    def _should_save(self, user: User) -> None:
        self._repository.should_save(user)

    def _should_match(self, criteria: Criteria, users: list[User]) -> None:
        self._repository.should_match(criteria, users)

    def _should_not_match(self, criteria: Criteria) -> None:
        self._repository.should_not_match(criteria)

    def _should_search_and_find(self, user: User) -> None:
        self._repository.should_search(user)

    def _should_search_and_not_find(self, user: User) -> None:
        self._repository.should_not_search(user)

    def _should_remove(self, user: User) -> None:
        self._repository.should_remove(user)
