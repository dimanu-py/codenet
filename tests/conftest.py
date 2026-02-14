from collections.abc import AsyncGenerator, Generator

import pytest
from dishka import Provider, Scope, make_async_container, provide, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.app.main import create_app
from src.auth.account.infra.injector.account_dependency_provider import AccountDependencyProvider
from src.backoffice.user.infra.injector.user_dependency_provider import UserDependencyProvider

pytest_plugins = [
    "tests.shared.infra.persistence.database_fixtures",
    "tests.backoffice.user.user_fixtures",
    "tests.auth.account.account_fixtures",
]


class TestSessionProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @provide
    def session(self) -> AsyncSession:
        return self._session


@pytest.fixture
def container(session: AsyncSession) -> Generator[AsyncContainer]:
    container = make_async_container(
        TestSessionProvider(session), AccountDependencyProvider(), UserDependencyProvider()
    )
    yield container
    container.close()


@pytest.fixture
async def client(container, session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    app = create_app()
    setup_dishka(container, app)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
