import pytest
from expects import be_empty, be_none, equal, expect
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmailAlreadyExists
from src.auth.account.domain.account_id import AccountId
from src.auth.account.domain.account_username import AccountUsernameAlreadyExists
from src.auth.account.domain.accounts import Accounts
from src.auth.account.infra.persistence.account_model import AccountModel
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.shared.domain.criteria.condition.operator import Operator
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.shared.domain.criteria.mothers.criteria_mother import CriteriaMother
from tests.shared.expects.matchers import async_expect, raise_error


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

    async def test_should_match_an_existing_account_based_on_criteria(self, existing_account: Account) -> None:
        criteria = CriteriaMother.with_one_condition(
            field="username", operator=Operator.EQUAL, value=existing_account._username.value
        )

        searched_accounts = await self._repository.matching(criteria)

        expect(searched_accounts).to(equal(Accounts([existing_account])))

    async def test_should_return_empty_list_if_no_accounts_match_criteria(self) -> None:
        criteria = CriteriaMother.empty()

        searched_accounts = await self._repository.matching(criteria)

        expect(searched_accounts).to(be_empty)

    async def test_should_not_allow_to_store_account_with_duplicated_email(self, existing_account_email: str) -> None:
        account_with_duplicated_email = AccountMother.create(email=existing_account_email)

        await async_expect(lambda: self._repository.save(account_with_duplicated_email)).to(
            raise_error(AccountEmailAlreadyExists)
        )

    async def test_should_not_allow_to_store_account_with_duplicated_username(
        self, existing_account_username: str
    ) -> None:
        account_with_duplicated_username = AccountMother.create(username=existing_account_username)

        await async_expect(lambda: self._repository.save(account_with_duplicated_username)).to(
            raise_error(AccountUsernameAlreadyExists)
        )

    async def _get_saved_account(self, account_id: AccountId) -> Account | None:
        account = await self._session.get(AccountModel, account_id.value)
        return account.to_domain() if account else None
