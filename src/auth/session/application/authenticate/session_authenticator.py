from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
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
        repository: AccountRepository,
        password_verifier: PasswordManager,
        token_issuer: TokenIssuer,
        credentials_finder: AccountCredentialsFinder | None = None,
    ) -> None:
        self._repository = repository
        self._password_verifier = password_verifier
        self._token_issuer = token_issuer
        self._credentials_finder = credentials_finder

    async def execute(self, identification: str, password: str) -> AuthenticationToken:
        signed_up_account = await self._ensure_account_exists_with(identification)
        await self._ensure_introduced_password_is_correct(password, signed_up_account)
        token = await self._issue_authentication_token_for(identification)
        return token

    async def _ensure_introduced_password_is_correct(self, password: str, account: Account) -> None:
        if not await account.verify_password(password, self._password_verifier):
            raise InvalidCredentials()

    async def _issue_authentication_token_for(self, identification: str) -> AuthenticationToken:
        token = await self._token_issuer.generate_token(identification)
        return AuthenticationToken(**token)

    async def _ensure_account_exists_with(self, identification: str) -> AccountAuthCredentials:
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
