import pytest
from expects import be_empty, equal, expect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from src.shared.domain.criteria.condition.operator import Operator
from src.shared.domain.value_objects.optional import Optional
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.shared.expects.matchers import async_expect, raise_error


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresUserRepository:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._repository = PostgresUserRepository(session)

    async def test_should_save_and_find_stored_user(self, existing_account_id: str) -> None:
        user = UserMother.with_id(existing_account_id)

        await self._repository.save(user)
        saved_user = await self._repository.search(user.username)

        expect(user).to(equal(saved_user.unwrap()))

    async def test_should_match_an_existing_user_based_on_criteria(self, existing_user: User) -> None:
        criteria = CriteriaMother.with_one_condition(
            field="username", operator=Operator.EQUAL, value=existing_user.username.value
        )

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(equal([existing_user]))

    async def test_should_return_empty_list_if_no_users_match_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(be_empty)

    async def test_should_delete_existing_user(self, existing_user: User) -> None:
        await self._repository.delete(existing_user.username)

        saved_user = await self._repository.search(existing_user.username)
        expect(saved_user).to(equal(Optional.empty()))

    async def test_should_raise_error_if_user_does_not_match_an_existing_account(self) -> None:
        user = UserMother.any()

        await async_expect(lambda: self._repository.save(user)).to(raise_error(IntegrityError))
