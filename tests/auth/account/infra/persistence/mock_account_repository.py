from unittest.mock import AsyncMock

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository


class MockAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()

    async def save(self, account: Account) -> None:
        await self._mock_save(account.to_primitives())

    def should_have_saved(self, account: dict) -> None:
        self._mock_save.assert_awaited_once_with(account)
