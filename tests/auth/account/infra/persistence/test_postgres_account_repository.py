import pytest
from expects import be_none, equal, expect
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_id import AccountId
from src.auth.account.infra.persistence.account_model import AccountModel
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

    async def test_should_search_and_find_an_existing_account_based_on_email(self, existing_account: Account) -> None:
        searched_account = await self._repository.search_by_email(existing_account._email)

        expect(searched_account.unwrap()).to(equal(existing_account))

    async def _get_saved_account(self, account_id: AccountId) -> Account | None:
        account = await self._session.get(AccountModel, account_id.value)
        return account.to_domain() if account else None
