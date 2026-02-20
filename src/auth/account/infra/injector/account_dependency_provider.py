from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.infra.api.authenticate.authenticate_account_controller import AuthenticateAccountController
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
    def signup_controller(self, account_repository: AccountRepository) -> SignupAccountController:
        password_manager = ArgonPasswordManager()
        clock = DatetimeClock()
        use_case = AccountSignup(repository=account_repository, password_manager=password_manager, clock=clock)
        return SignupAccountController(use_case=use_case)

    @provide
    def authenticate_controller(self) -> AuthenticateAccountController:
        return AuthenticateAccountController()