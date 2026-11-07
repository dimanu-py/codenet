import pytest

from src.auth.account.domain.account import Account, AccountPrimitives
from src.auth.account.infra.persistence.account_model import AccountModel
from tests.auth.account.domain.mothers.account_mother import AccountPrimitivesMother


@pytest.fixture
async def existing_account(add_to_database) -> AccountPrimitives:
    account_primitives = AccountPrimitivesMother.dummy()
    await add_to_database(AccountModel.from_domain(Account(**account_primitives)))
    return account_primitives
