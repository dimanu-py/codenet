from collections.abc import AsyncGenerator

import pytest
from dishka.integrations.fastapi import setup_dishka
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.app.main import create_app
from tests.shared.infra.injector.di_fixtures import container

pytest_plugins = [
    "tests.shared.infra.persistence.database_fixtures",
    "tests.shared.infra.injector.di_fixtures",
    "tests.backoffice.user.user_fixtures",
    "tests.auth.account.account_fixtures",
]


@pytest.fixture
async def client(container, session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    app = create_app()
    setup_dishka(container, app)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
