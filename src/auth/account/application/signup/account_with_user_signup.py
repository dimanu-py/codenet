from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository


class AccountWithUserSignup:
    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        account_id: str,
        name: str,
        username: str,
        email: str,
        plain_password: str,
    ) -> None:
        await self._signup_account_with(
            account_id=account_id,
            email=email,
            plain_password=plain_password,
        )
        await self._signup_user_with(
            user_id=account_id,
            name=name,
            username=username,
            email=email,
        )

    async def _signup_user_with(self, user_id: str, name: str, username: str, email: str) -> None:
        pass

    async def _signup_account_with(self, account_id: str, email: str, plain_password: str) -> None:
        account = Account.signup(id=account_id, email=email, password=plain_password)
        await self._repository.save(account)