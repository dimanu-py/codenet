from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.backoffice.user.application.removal.user_remover import UserRemover
from src.backoffice.user.application.search.user_searcher import UserSearcher
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.infra.api.removal.user_removal_controller import UserRemovalController
from src.backoffice.user.infra.api.search.user_search_controller import UserSearchController
from src.backoffice.user.infra.persistence.postgres_user_repository import PostgresUserRepository


class UserDependencyProvider(Provider):
    scope = Scope.REQUEST

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
