import pytest
from expects import expect, equal
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.shared.infra.settings import Settings
from src.social.user.infra.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.user.domain.user_mother import UserMother


@pytest.fixture
async def engine() -> AsyncEngine:
    settings = Settings()
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

        saved_user = await repository.search(user.id)
        expect(user).to(equal(saved_user))
