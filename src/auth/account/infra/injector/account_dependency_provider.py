from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.infra.api.signup.signup_account_controller import SignupAccountController
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.auth.shared.domain.password_manager import PasswordManager
from src.auth.shared.infra.argon_password_manager import ArgonPasswordManager
from src.shared.infra.datetime_clock import DatetimeClock
from src.shared.infra.injector.registry import dependency_provider


@dependency_provider
class AccountDependencyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def account_repository(self, session: AsyncSession) -> AccountRepository:
        return PostgresAccountRepository(session=session)

    @provide
    def password_hasher(self) -> PasswordManager:
        return ArgonPasswordManager()

    @provide
    def signup_controller(
        self, account_repository: AccountRepository, password_hasher: PasswordManager
    ) -> SignupAccountController:
        return SignupAccountController(
            use_case=AccountSignup(
                repository=account_repository, password_hasher=password_hasher, clock=DatetimeClock()
            )
        )
