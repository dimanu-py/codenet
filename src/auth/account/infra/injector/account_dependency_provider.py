from collections.abc import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.password_manager import PasswordManager
from src.auth.account.infra.api.signup.signup_controller import SignupController
from src.auth.account.infra.argon_password_manager import ArgonPasswordManager
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.backoffice.user.application.signup.user_signup import UserSignup
from src.backoffice.user.infra.persistence.postgres_user_repository import PostgresUserRepository
from src.shared.delivery.settings import Settings
from src.shared.domain.clock import Clock
from src.shared.infra.datetime_clock import DatetimeClock


class AccountDependencyProvider(Provider):
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
    def account_repository(self, session: AsyncSession) -> AccountRepository:
        return PostgresAccountRepository(session=session)

    @provide
    def user_repository(self, session: AsyncSession) -> PostgresUserRepository:
        return PostgresUserRepository(session=session)

    @provide
    def user_signup(self, repository: PostgresUserRepository) -> UserSignup:
        return UserSignup(repository=repository)

    @provide
    def password_manager(self) -> PasswordManager:
        return ArgonPasswordManager()

    @provide
    def clock(self) -> Clock:
        return DatetimeClock()

    @provide
    def account_with_user_signup(
        self, repository: AccountRepository, user_signup: UserSignup, password_manager: PasswordManager, clock: Clock
    ) -> AccountWithUserSignup:
        return AccountWithUserSignup(
            repository=repository,
            user_signup=user_signup,
            password_manager=password_manager,
            clock=clock,
        )

    @provide
    def signup_controller(self, use_case: AccountWithUserSignup) -> SignupController:
        return SignupController(use_case=use_case)
