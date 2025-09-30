from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine, AsyncConnection
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy_utils import create_database, database_exists

from src.delivery.main import app
from src.shared.infra.persistence.sqlalchemy.base import Base
from src.social.user.infra.api.deps import get_async_session


@pytest.fixture
def async_engine() -> AsyncEngine:
    return create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )


@pytest.fixture
async def setup_database(async_engine: AsyncEngine) -> AsyncGenerator[None]:
    if not database_exists(async_engine.url):
        create_database(async_engine.url)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def connection(
    async_engine: AsyncEngine,
    setup_database: None,  # noqa: ARG001
) -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as conn:
        yield conn


@pytest.fixture
async def session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=connection) as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


@pytest.fixture
@pytest.mark.asyncio
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def get_override_session() -> AsyncSession:
        return session

    app.dependency_overrides[get_async_session] = get_override_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
