from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmailAlreadyExists
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.account_username import AccountUsernameAlreadyExists
from src.auth.account.domain.password_manager import PasswordManager
from src.shared.domain.clock import Clock
from src.shared.domain.criteria.condition.operator import Operator
from src.shared.domain.criteria.criteria import Criteria


class AccountSignup:
    def __init__(self, repository: AccountRepository, password_manager: PasswordManager, clock: Clock) -> None:
        self._repository = repository
        self._clock = clock
        self._password_manager = password_manager

    async def execute(self, account_id: str, username: str, email: str, plain_password: str) -> None:
        await self._ensure_account_with_same_email_is_not_already_signed_up(email)
        await self._ensure_account_with_same_username_is_not_already_signed_up(username)
        hashed_password = await self._hash_account_password(plain_password)
        await self._signup_account_with(account_id=account_id, username=username, email=email, password=hashed_password)

    async def _hash_account_password(self, password: str) -> str:
        return await self._password_manager.hash(password)

    async def _signup_account_with(self, account_id: str, username: str, email: str, password: str) -> None:
        account = Account.signup(id=account_id, username=username, email=email, password=password, clock=self._clock)
        await self._repository.save(account)

    async def _ensure_account_with_same_email_is_not_already_signed_up(self, email: str) -> None:
        signed_up_accounts = await self._repository.matching(
            criteria=Criteria.from_primitives(filter_expression={"field": "email", Operator.EQUAL: email})
        )
        if signed_up_accounts.is_not_empty():
            raise AccountEmailAlreadyExists()

    async def _ensure_account_with_same_username_is_not_already_signed_up(self, username: str) -> None:
        signed_up_accounts = await self._repository.matching(
            criteria=Criteria.from_primitives(filter_expression={"field": "username", Operator.EQUAL: username})
        )
        if signed_up_accounts.is_not_empty():
            raise AccountUsernameAlreadyExists()
