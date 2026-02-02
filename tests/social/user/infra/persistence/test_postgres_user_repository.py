import pytest
from expects import be_empty, equal, expect
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.domain.criteria.condition.operator import Operator
from src.shared.domain.value_objects.optional import Optional
from src.social.user.domain.user import User
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.social.user.domain.mothers.user_mother import UserMother


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresUserRepository:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._repository = PostgresUserRepository(session)

    async def test_should_save_and_find_existing_user(self) -> None:
        user = UserMother.any()

        await self._repository.save(user)
        saved_user = await self._repository.search(user.username)

        expect(user).to(equal(saved_user.unwrap()))

    async def test_should_match_a_user_based_on_criteria(self) -> None:
        user = await self._given_an_user_already_exists()
        criteria = CriteriaMother.with_one_condition(
            field="username", operator=Operator.EQUAL, value=user.username.value
        )

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(equal([user]))

    async def test_should_return_empty_list_if_no_users_are_found(self) -> None:
        criteria = CriteriaMother.empty()

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(be_empty)

    async def test_should_delete_existing_user(self) -> None:
        user = await self._given_an_user_already_exists()

        await self._repository.delete(user.username)

        await self._should_have_deleted(user)

    async def _should_have_deleted(self, user: User) -> None:
        saved_user = await self._repository.search(user.username)
        expect(saved_user).to(equal(Optional.empty()))

    async def _given_an_user_already_exists(self) -> User:
        user = UserMother.any()
        await self._repository.save(user)
        return user
