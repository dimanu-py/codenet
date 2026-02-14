from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession


class TestDatabaseSessionProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @provide
    def session(self) -> AsyncSession:
        return self._session
