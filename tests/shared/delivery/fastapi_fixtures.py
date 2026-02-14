from typing import AsyncGenerator

import pytest
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.main import create_app


@pytest.fixture
async def client(container: AsyncContainer, session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    app = create_app()
    setup_dishka(container, app)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
