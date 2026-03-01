import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.infra.service.postgres_account_credentials_finder import PostgresAccountCredentialsFinder


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresAccountCredentialsFinder:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = PostgresAccountCredentialsFinder(session)

    async def test_should_return_credentials_of_an_existing_account_using_email(self, existing_account_email: str) -> None:

