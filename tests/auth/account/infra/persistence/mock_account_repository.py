from typing import override
from unittest.mock import AsyncMock

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.accounts import Accounts
from src.shared.domain.criteria.criteria import Criteria
from src.shared.domain.value_objects.optional import Optional


class MockAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()
        self._mock_search = AsyncMock()

    @override
    async def save(self, account: Account) -> None:
        await self._mock_save(account)

    @override
    async def matching(self, criteria: Criteria) -> Accounts:
        pass

    @override
    async def search_by_email(self, email: AccountEmail) -> Optional[Account]:
        await self._mock_search(email)
        return self._mock_search.return_value

    def should_have_saved(self, account: Account) -> None:
        self._mock_save.assert_awaited_once_with(account)

    def should_search(self, account: Account) -> None:
        self._mock_search.return_value = Optional.of(account)

    def should_not_search_account(self) -> None:
        self._mock_search.return_value = Optional.empty()

    def should_not_have_saved_account(self) -> None:
        self._mock_save.assert_not_awaited()
