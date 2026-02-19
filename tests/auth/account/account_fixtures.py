import pytest

from src.auth.account.domain.account import Account
from src.auth.account.infra.persistence.account_model import AccountModel
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.domain.mothers.account_username_primitives_mother import AccountUsernamePrimitivesMother


@pytest.fixture
async def existing_account(add_to_database) -> Account:
    account = AccountMother.any()
    await add_to_database(AccountModel.from_domain(account))
    return account


@pytest.fixture
async def existing_account_id(add_to_database) -> str:
    account_id = AccountIdPrimitivesMother.any()
    account = AccountMother.create(id=account_id)
    await add_to_database(AccountModel.from_domain(account))
    return account_id


@pytest.fixture
async def existing_account_ids(add_to_database, request) -> list[str]:
    """Create multiple accounts and return their IDs.

    Use with pytest.mark.parametrize on 'request' or by passing count directly.
    Example: @pytest.mark.parametrize('existing_account_ids', [3], indirect=True)
    """
    count = getattr(request, "param", 3)
    account_ids = []
    for _ in range(count):
        account_id = AccountIdPrimitivesMother.any()
        account = AccountMother.create(id=account_id)
        await add_to_database(AccountModel.from_domain(account))
        account_ids.append(account_id)
    return account_ids


@pytest.fixture
async def existing_account_email(add_to_database) -> str:
    email = AccountEmailPrimitivesMother.any()
    account = AccountMother.create(email=email)
    await add_to_database(AccountModel.from_domain(account))
    return email


@pytest.fixture
async def existing_account_username(add_to_database) -> str:
    username = AccountUsernamePrimitivesMother.any()
    account = AccountMother.create(username=username)
    await add_to_database(AccountModel.from_domain(account))
    return username
