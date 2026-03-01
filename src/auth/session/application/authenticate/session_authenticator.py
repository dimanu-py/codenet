from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.account_credentials_finder import AccountCredentialsFinder
from src.auth.session.domain.login_identifier import LoginIdentifier
from src.auth.session.domain.token_issuer import TokenIssuer
from src.auth.session.infra.authentication_token import AuthenticationToken
from src.auth.shared.domain.password_manager import PasswordManager
from src.shared.domain.exceptions.domain_error import DomainError


class SessionAuthenticator:
    def __init__(
        self,
        credentials_finder: AccountCredentialsFinder,
        password_verifier: PasswordManager,
        token_issuer: TokenIssuer,
    ) -> None:
        self._credentials_finder = credentials_finder
        self._password_verifier = password_verifier
        self._token_issuer = token_issuer

    async def execute(self, identification: str, password: str) -> AuthenticationToken:
        account_auth_credentials = await self._ensure_account_exists_with_identification(identification)
        await self._ensure_introduced_password_is_correct(password, account_auth_credentials)
        token = await self._issue_authentication_token_for(identification)
        return token

    async def _ensure_introduced_password_is_correct(
        self, password: str, account_auth_credentials: AccountAuthCredentials
    ) -> None:
        if not await account_auth_credentials.verify_password(password, self._password_verifier):
            raise InvalidCredentials()

    async def _issue_authentication_token_for(self, identification: str) -> AuthenticationToken:
        token = await self._token_issuer.generate_token(identification)
        return AuthenticationToken(**token)

    async def _ensure_account_exists_with_identification(self, identification: str) -> AccountAuthCredentials:
        account_auth_credentials = await self._credentials_finder.find_by_login_identifier(
            login=LoginIdentifier(identification)
        )
        return account_auth_credentials.unwrap_or_raise(InvalidCredentials)


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_type="invalid_credentials",
        )
