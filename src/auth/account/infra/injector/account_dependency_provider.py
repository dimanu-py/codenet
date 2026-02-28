from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.password_manager import PasswordManager
from src.auth.account.infra.api.signup.signup_account_controller import SignupAccountController
from src.auth.account.infra.argon_password_manager import ArgonPasswordManager
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.shared.infra.datetime_clock import DatetimeClock
from src.shared.infra.injector.registry import register_provider


@register_provider
class AccountDependencyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def account_repository(self, session: AsyncSession) -> AccountRepository:
        return PostgresAccountRepository(session=session)

    @provide
    def password_manager(self) -> PasswordManager:
        return ArgonPasswordManager()

    @provide
    def signup_controller(
        self, account_repository: AccountRepository, password_manager: PasswordManager
    ) -> SignupAccountController:
        return SignupAccountController(
            use_case=AccountSignup(
                repository=account_repository, password_manager=password_manager, clock=DatetimeClock()
            )
        )
