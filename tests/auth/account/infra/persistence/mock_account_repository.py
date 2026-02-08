from unittest.mock import AsyncMock

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_repository import AccountRepository
from src.shared.domain.value_objects.optional import Optional


class MockAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()

    async def save(self, account: Account) -> None:
        await self._mock_save(account)

    async def search_by_email(self, email: AccountEmail) -> Optional[Account]:
        pass

    def should_have_saved(self, account: Account) -> None:
        self._mock_save.assert_awaited_once_with(account)
