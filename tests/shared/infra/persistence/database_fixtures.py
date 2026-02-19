from collections.abc import AsyncGenerator, Generator, Callable, Coroutine
from typing import Any

import pytest
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shared.infra.persistence.sqlalchemy.base import Base
from tests.shared.infra.persistence.postgres_test_container import PostgresTestContainer


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
    nested_transaction = await connection.begin_nested()

    async with AsyncSession(bind=connection) as session:
        yield session

    await nested_transaction.rollback()


@pytest.fixture
async def add_to_database(session: AsyncSession) -> Callable[..., Coroutine[Any, Any, None]]:
    async def _insert(values) -> None:
        session.add(values)
        await session.commit()
    return _insert
