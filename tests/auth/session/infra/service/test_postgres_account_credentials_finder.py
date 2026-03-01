import pytest
from expects import expect, be_none
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.domain.login_identifier import LoginIdentifier
from src.auth.session.infra.service.postgres_account_credentials_finder import PostgresAccountCredentialsFinder


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresAccountCredentialsFinder:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._credentials_finder = PostgresAccountCredentialsFinder(session)

    async def test_should_return_account_credentials_of_an_existing_account_using_email(
        self, existing_account_email: str
    ) -> None:
        login_identifier = LoginIdentifier(existing_account_email)

        account_auth_credentials = await self._credentials_finder.find_by_login_identifier(login_identifier)

        expect(account_auth_credentials).to_not(be_none)
