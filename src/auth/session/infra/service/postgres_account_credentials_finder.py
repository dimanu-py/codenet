from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.account_credentials_finder import AccountCredentialsFinder
from src.auth.session.domain.login_identifier import LoginIdentifier


class PostgresAccountCredentialsFinder(AccountCredentialsFinder):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def find_by_login_identifier(self, login: LoginIdentifier) -> AccountAuthCredentials | None:
        pass

