import pytest

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from tests.social.user.infra.persistence.mock_user_repository import MockUserRepository


@pytest.mark.unit
@pytest.mark.asyncio
class UserModuleUnitTestConfig:
    _repository = MockUserRepository()

    def _should_save(self, user: User) -> None:
        self._repository.should_save(user)

    def _should_match(self, criteria: Criteria, users: list[User]) -> None:
        self._repository.should_match(criteria, users)

    def _should_not_match(self, criteria: Criteria) -> None:
        self._repository.should_not_match(criteria)
