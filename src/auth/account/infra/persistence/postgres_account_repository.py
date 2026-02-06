from typing import override

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository


class PostgresAccountRepository(AccountRepository):
    @override
    async def save(self, account: Account) -> None:
        raise NotImplementedError
