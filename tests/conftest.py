from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.delivery.main import app
from src.shared.infra.persistence.sqlalchemy.base import Base
from src.social.user.infra.api.deps import get_async_session
from tests.social.user.infra.persistence.postgres_test_container import PostgresTestContainer


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresTestContainer]:
    container = PostgresTestContainer()
    container.start()
    yield container
    container.stop()


@pytest.fixture
def async_engine(postgres_container: PostgresTestContainer) -> AsyncEngine:
    return create_async_engine(
        postgres_container.get_base_url(),
        echo=False,
    )


@pytest.fixture
async def setup_database(async_engine: AsyncEngine) -> AsyncGenerator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def connection(
    async_engine: AsyncEngine,
    setup_database: None,  # noqa: ARG001
) -> AsyncGenerator[AsyncConnection]:
    async with async_engine.connect() as conn:
        yield conn


@pytest.fixture
async def session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(bind=connection) as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    def get_override_session() -> AsyncSession:
        return session

    app.dependency_overrides[get_async_session] = get_override_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
