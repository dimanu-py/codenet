from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infra.injector.registry import get_registered_providers, register_providers
from tests.shared.infra.injector.test_database_session_provider import TestDatabaseSessionProvider


@pytest.fixture
async def container(session: AsyncSession) -> AsyncGenerator[AsyncContainer]:
    register_providers()
    container = make_async_container(*get_registered_providers(), TestDatabaseSessionProvider(session))
    yield container
    await container.close()
