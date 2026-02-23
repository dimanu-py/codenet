from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.delivery.settings import Settings


class TestDatabaseSessionProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @provide
    def session(self) -> AsyncSession:
        return self._session

    @provide
    def settings(self) -> Settings:
        return Settings()
