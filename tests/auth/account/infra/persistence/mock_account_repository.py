from typing import override
from unittest.mock import AsyncMock

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_repository import AccountRepository
from src.auth.account.domain.accounts import Accounts
from src.shared.domain.criteria.criteria import Criteria


class MockAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._mock_save = AsyncMock()
        self._mock_match = AsyncMock()

    @override
    async def save(self, account: Account) -> None:
        await self._mock_save(account)

    @override
    async def matching(self, criteria: Criteria) -> Accounts:
        await self._mock_match(criteria)
        return self._mock_match.return_value

    def should_have_saved(self, account: Account) -> None:
        self._mock_save.assert_awaited_once_with(account)

    def should_not_have_saved_account(self) -> None:
        self._mock_save.assert_not_awaited()

    def should_match_criteria_with(self, accounts: list[Account]) -> None:
        self._mock_match.return_value = Accounts(accounts)

    def should_not_match_criteria(self) -> None:
        self._mock_match.return_value = Accounts([])
