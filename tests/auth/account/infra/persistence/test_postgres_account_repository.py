import pytest
from expects import expect, equal, be_none
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_id import AccountId
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from tests.auth.account.domain.mothers.account_mother import AccountMother


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresAccountRepository:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = PostgresAccountRepository(session)

    async def test_should_save_and_find_stored_account(self) -> None:
        account = AccountMother.any()

        await self._repository.save(account)
        saved_account = await self._get_saved_account(account.id)

        expect(saved_account).to_not(be_none)
        expect(account).to(equal(saved_account))

    async def _get_saved_account(self, account_id: AccountId) -> Account | None:
        pass