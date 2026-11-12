from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.session.domain.account_by_login_identifier_criteria import AccountByLoginIdentifierCriteria
from src.auth.session.domain.token_issuer import TokenIssuer
from src.auth.session.infra.authentication_token import AuthenticationToken
from src.auth.shared.domain.password_manager import PasswordManager
from src.shared.domain.exceptions.domain_error import DomainError


class SessionAuthenticator:
    def __init__(
        self, password_verifier: PasswordManager, token_issuer: TokenIssuer, account_repository: AccountRepository
    ) -> None:
        self._password_verifier = password_verifier
        self._token_issuer = token_issuer
        self._account_repository = account_repository

    async def execute(self, identification: str, password: str) -> AuthenticationToken:
        exiting_account = await self._ensure_account_exists_with_identification(identification)
        await self._ensure_introduced_password_is_correct(password, exiting_account)
        token = await self._issue_authentication_token_for(exiting_account)
        return token

    async def _ensure_introduced_password_is_correct(self, password: str, account: Account) -> None:
        if await account.password_is_incorrect(password, self._password_verifier):
            raise InvalidCredentials()

    async def _issue_authentication_token_for(self, account: Account) -> AuthenticationToken:
        token = await self._token_issuer.generate_token(account.id.value)
        return AuthenticationToken(**token)

    async def _ensure_account_exists_with_identification(self, identification: str) -> Account:
        criteria = AccountByLoginIdentifierCriteria.for_login_identifier(login=identification)
        candidate_accounts = await self._account_repository.matching(criteria)
        if candidate_accounts.has_accounts():
            return candidate_accounts.first()
        raise InvalidCredentials()


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_type="invalid_credentials",
        )
