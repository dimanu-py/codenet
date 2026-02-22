from src.auth.account.domain.password_manager import PasswordManager
from src.auth.account.domain.token_issuer import TokenIssuer
from src.shared.domain.exceptions.domain_error import DomainError


class AccountAuthenticator:
    def __init__(self, password_manager: PasswordManager, token_issuer: TokenIssuer) -> None:
        self._password_manager = password_manager
        self._token_issuer = token_issuer

    async def execute(self, identification: str, password: str) -> str:
        pass


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_type="invalid_credentials",
        )
