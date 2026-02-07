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

    async def test_should_match_an_existing_user_based_on_criteria(self, existing_account_id: str) -> None:
        user = await self._given_an_user_already_exists(existing_account_id)
        criteria = CriteriaMother.with_one_condition(
            field="username", operator=Operator.EQUAL, value=user.username.value
        )

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(equal([user]))

    async def test_should_return_empty_list_if_no_users_match_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        searched_users = await self._repository.matching(criteria)

        expect(searched_users).to(be_empty)

    async def test_should_delete_existing_user(self, existing_account_id: str) -> None:
        user = await self._given_an_user_already_exists(existing_account_id)

        await self._repository.delete(user.username)

        await self._should_have_deleted(user)

    async def test_should_raise_error_if_user_does_not_match_existing_an_account(self) -> None:
        user = UserMother.any()

        with pytest.raises(IntegrityError):
            await self._repository.save(user)

    async def _should_have_deleted(self, user: User) -> None:
        saved_user = await self._repository.search(user.username)
        expect(saved_user).to(equal(Optional.empty()))

    async def _given_an_user_already_exists(self, user_id: str) -> User:
        user = UserMother.with_id(user_id)
        await self._repository.save(user)
        return user
