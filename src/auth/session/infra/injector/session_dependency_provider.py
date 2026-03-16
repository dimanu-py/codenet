from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.application.authenticate import SessionAuthenticator
from src.auth.session.infra.api.authenticate.authenticate_session_controller import AuthenticateSessionController
from src.auth.session.infra.jwt_token_issuer import JwtTokenIssuer
from src.auth.session.infra.service.postgres_account_credentials_finder import PostgresAccountCredentialsFinder
from src.auth.shared.infra.argon_password_manager import ArgonPasswordManager
from src.shared.delivery.settings import Settings
from src.shared.infra.injector.registry import dependency_provider


@dependency_provider
class SessionDependencyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def account_credentials_finder(self, session: AsyncSession) -> PostgresAccountCredentialsFinder:
        return PostgresAccountCredentialsFinder(session=session)

    @provide
    def authenticate_controller(
        self, account_credentials_finder: PostgresAccountCredentialsFinder, settings: Settings
    ) -> AuthenticateSessionController:
        return AuthenticateSessionController(
            use_case=SessionAuthenticator(
                credentials_finder=account_credentials_finder,
                password_verifier=ArgonPasswordManager(),
                token_issuer=JwtTokenIssuer(settings=settings),
            ),
        )
