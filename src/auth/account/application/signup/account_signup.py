from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.shared.domain.password_manager import PasswordManager
from src.shared.domain.clock import Clock
from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.criteria.filter import Filter, Filters
from src.shared.domain.criteria.operator import Operator
from src.shared.domain.exceptions.domain_error import ConflictError


class AccountSignup:
    def __init__(self, repository: AccountRepository, password_hasher: PasswordManager, clock: Clock) -> None:
        self._repository = repository
        self._clock = clock
        self._password_hasher = password_hasher

    async def execute(self, account_id: str, username: str, email: str, plain_password: str) -> None:
        await self._ensure_account_with_same_email_or_username_is_not_already_signed_up(email, username)
        hashed_password = await self._hash_account_password(plain_password)
        await self._signup_account_with(account_id=account_id, username=username, email=email, password=hashed_password)

    async def _hash_account_password(self, password: str) -> str:
        return await self._password_hasher.hash(password)

    async def _signup_account_with(self, account_id: str, username: str, email: str, password: str) -> None:
        account = Account.signup(id=account_id, username=username, email=email, password=password, clock=self._clock)
        await self._repository.save(account)

    async def _ensure_account_with_same_email_or_username_is_not_already_signed_up(
        self, email: str, username: str
    ) -> None:
        has_email = Criteria(filters=Filters([Filter(field="email", operator=Operator.EQUALS, value=email)]))
        has_username = Criteria(filters=Filters([Filter(field="username", operator=Operator.EQUALS, value=username)]))
        signed_up_accounts = await self._repository.matching(criteria=has_email | has_username)
        if signed_up_accounts.has_accounts():
            if signed_up_accounts.has_email(email):
                raise AccountEmailAlreadyExists()
            if signed_up_accounts.has_username(username):
                raise AccountUsernameAlreadyExists()


class AccountEmailAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(message="Email is already signed up")


class AccountUsernameAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(message="Username is already registered.")
