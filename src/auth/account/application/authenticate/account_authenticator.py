from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.password_manager import PasswordManager
from src.auth.account.domain.token_issuer import TokenIssuer
from src.auth.account.infra.authentication_token import AuthenticationToken
from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.exceptions.domain_error import DomainError


class AccountAuthenticator:
    def __init__(
        self, repository: AccountRepository, password_manager: PasswordManager, token_issuer: TokenIssuer
    ) -> None:
        self._repository = repository
        self._password_manager = password_manager
        self._token_issuer = token_issuer

    async def execute(self, identification: str, password: str) -> AuthenticationToken:
        existing_account = await self._ensure_account_exists_with(identification)
        await self._ensure_introduced_password_is_correct(password, existing_account._password.value)
        token = await self._issue_authentication_token_for(identification)
        return token

    async def _ensure_introduced_password_is_correct(self, password: str, account_password: str) -> None:
        if not await self._password_manager.verify_credentials(password=password, stored_password=account_password):
            raise InvalidCredentials()

    async def _issue_authentication_token_for(self, identification: str) -> AuthenticationToken:
        token = await self._token_issuer.generate_token(identification)
        return AuthenticationToken(**token)

    async def _ensure_account_exists_with(self, identification: str) -> Account:
        existing_accounts = await self._repository.matching(
            criteria=Criteria.from_primitives(
                filter_expression={
                    "or": [
                        {"field": "email", "equal": identification},
                        {"field": "username", "equal": identification},
                    ]
                }
            )
        )
        if existing_accounts.is_empty():
            raise InvalidCredentials()
        return existing_accounts.first()


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_type="invalid_credentials",
        )
