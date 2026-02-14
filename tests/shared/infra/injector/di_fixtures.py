from collections.abc import Generator

import pytest
from dishka import AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.infra.injector.account_dependency_provider import AccountDependencyProvider
from src.backoffice.user.infra.injector.user_dependency_provider import UserDependencyProvider
from tests.shared.infra.injector.test_database_session_provider import TestDatabaseSessionProvider


@pytest.fixture
def container(session: AsyncSession) -> Generator[AsyncContainer]:
    container = make_async_container(
        TestDatabaseSessionProvider(session), AccountDependencyProvider(), UserDependencyProvider()
    )
    yield container
    container.close()
