from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository


class MockAccountRepository(AccountRepository):

    async def save(self, account: Account) -> None:
        pass
