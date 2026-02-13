from collections.abc import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from src.backoffice.user.application.removal.user_remover import UserRemover
from src.backoffice.user.application.search.user_searcher import UserSearcher
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.infra.api.removal.user_removal_controller import UserRemovalController
from src.backoffice.user.infra.api.search.user_search_controller import UserSearchController
from src.backoffice.user.infra.persistence.postgres_user_repository import PostgresUserRepository
from src.shared.delivery.settings import Settings


class UserDependencyProvider(Provider):
    scope = Scope.REQUEST

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

    @provide
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return PostgresUserRepository(session=session)

    @provide
    def user_remover(self, repository: UserRepository) -> UserRemover:
        return UserRemover(repository=repository)

    @provide
    def removal_controller(self, use_case: UserRemover) -> UserRemovalController:
        return UserRemovalController(use_case=use_case)

    @provide
    def user_searcher(self, repository: UserRepository) -> UserSearcher:
        return UserSearcher(repository=repository)

    @provide
    def search_controller(self, use_case: UserSearcher) -> UserSearchController:
        return UserSearchController(use_case=use_case)
