from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.password_manager import PasswordManager
from src.shared.domain.clock import Clock
from src.backoffice.user.application.signup.user_signup import UserSignup


class AccountWithUserSignup:
    def __init__(self, repository: AccountRepository, user_signup: UserSignup, password_manager: PasswordManager, clock: Clock) -> None:
        self._repository = repository
        self._user_signup = user_signup
        self._clock = clock
        self._password_manager = password_manager

    async def execute(
        self,
        account_id: str,
        name: str,
        username: str,
        email: str,
        plain_password: str,
    ) -> None:
        hashed_password = self._hash_account_password(plain_password)
        await self._signup_account_with(
            account_id=account_id,
            email=email,
            password=hashed_password,
        )
        await self._signup_user_with(
            user_id=account_id,
            name=name,
            username=username,
        )

    def _hash_account_password(self, password: str) -> str:
        return self._password_manager.hash(password)

    async def _signup_user_with(self, user_id: str, name: str, username: str) -> None:
        await self._user_signup.execute(
            id=user_id,
            name=name,
            username=username,
        )

    async def _signup_account_with(self, account_id: str, email: str, password: str) -> None:
        account = Account.signup(id=account_id, email=email, password=password, clock=self._clock)
        await self._repository.save(account)
