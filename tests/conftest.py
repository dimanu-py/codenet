from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.app.main import app
from src.shared.delivery.db_session import get_async_session

pytest_plugins = ["tests.shared.infra.database_fixtures", "tests.backoffice.user.user_fixtures"]


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    def get_override_session() -> AsyncSession:
        return session

    app.dependency_overrides[get_async_session] = get_override_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
