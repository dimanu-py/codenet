from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.shared.delivery.settings import Settings


class DatabaseSessionProvider(Provider):
    scope = Scope.APP

    @provide
    def settings(self) -> Settings:
        return Settings()  # type: ignore[call-arg]

    @provide
    def engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(str(settings.postgres_url), echo=False)

    @provide
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
