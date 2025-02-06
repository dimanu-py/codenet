from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)

from src.shared.infra.persistence.sqlalchemy.base import (
    Base,
)
from src.shared.infra.settings import Settings


class SessionMaker:
    _session_maker: async_sessionmaker[AsyncSession]
    _engine: AsyncEngine

    def __init__(self, settings: Settings) -> None:
        self._engine = create_async_engine(settings.postgres_url)
        self._session_maker = async_sessionmaker(bind=self._engine)

    def get_session(self) -> AsyncSession:
        return self._session_maker()

    async def create_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
