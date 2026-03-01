from typing import override
from unittest.mock import AsyncMock

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.account_credentials_finder import AccountCredentialsFinder
from src.auth.session.domain.login_identifier import LoginIdentifier
from src.shared.domain.value_objects.optional import Optional


class MockAccountCredentialsFinder(AccountCredentialsFinder):
    def __init__(self) -> None:
        self._mock_find = AsyncMock()

    @override
    async def find_by_login_identifier(self, login: LoginIdentifier) -> Optional[AccountAuthCredentials]:
        return await self._mock_find(login)

    def should_search_and_find_account_auth_credentials(self, account_auth_credentials: AccountAuthCredentials) -> None:
        self._mock_find.return_value = Optional.of(account_auth_credentials)
