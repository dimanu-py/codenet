from collections.abc import AsyncGenerator

import pytest
from expects import expect, equal, be_empty
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.shared.infra.settings import Settings
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.shared.domain.criteria.criteria_mother import CriteriaMother
from tests.social.user.domain.user_mother import UserMother


@pytest.fixture
async def engine() -> AsyncGenerator[AsyncEngine]:
    settings = Settings()  # type: ignore
    engine = create_async_engine(settings.postgres_url)

    async with engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.drop_all)
    await engine.dispose()


@pytest.mark.integration
class TestPostgresUserRepository:
    @pytest.mark.asyncio
    async def test_should_save_user(self, engine: AsyncEngine) -> None:
        repository = PostgresUserRepository(engine)
        user = UserMother.any()

        await repository.save(user)

    @pytest.mark.asyncio
    async def test_should_find_existing_user(self, engine: AsyncEngine) -> None:
        repository = PostgresUserRepository(engine)
        user = UserMother.any()
        await repository.save(user)

        saved_user = await repository.find(user.id)

        expect(user).to(equal(saved_user))

    @pytest.mark.asyncio
    async def test_should_match_a_user_based_on_criteria(
        self, engine: AsyncEngine
    ) -> None:
        repository = PostgresUserRepository(engine)
        user = UserMother.any()
        criteria = CriteriaMother.with_one_filter(
            field="username", operator="eq", value=user.username.value
        )
        await repository.save(user)

        searched_users = await repository.matching(criteria)

        expect(searched_users).to(equal([user]))

    @pytest.mark.asyncio
    async def test_should_return_empty_list_if_no_users_are_found(self, engine: AsyncEngine) -> None:
        repository = PostgresUserRepository(engine)
        criteria = CriteriaMother.any()

        searched_users = await repository.matching(criteria)

        expect(searched_users).to(be_empty)