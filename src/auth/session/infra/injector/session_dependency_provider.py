from dishka import Provider, Scope, provide

from src.auth.account.domain.account_repository import AccountRepository
from src.auth.session.application.session_authenticator import SessionAuthenticator
from src.auth.session.infra.api.authenticate_session_controller import AuthenticateSessionController
from src.auth.session.infra.jwt_token_issuer import JwtTokenIssuer
from src.auth.shared.infra.argon_password_manager import ArgonPasswordManager
from src.shared.delivery.settings import Settings
from src.shared.infra.injector.provider_registry import dependency_provider


@dependency_provider
class SessionDependencyProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def authenticate_controller(
        self,
        settings: Settings,
        account_repository: AccountRepository,
    ) -> AuthenticateSessionController:
        return AuthenticateSessionController(
            use_case=SessionAuthenticator(
                password_verifier=ArgonPasswordManager(),
                token_issuer=JwtTokenIssuer(settings=settings),
                account_repository=account_repository,
            ),
        )
