import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.infra.persistence.account_model import AccountModel
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother


@pytest.fixture
async def existing_account_id(session: AsyncSession) -> str:
    account_id = AccountIdPrimitivesMother.any()
    account = AccountMother.with_id(account_id)
    session.add(AccountModel.from_domain(account))
    await session.commit()
    return account_id


@pytest.fixture
async def existing_account_ids(session: AsyncSession, request) -> list[str]:
    """Create multiple accounts and return their IDs.

    Use with pytest.mark.parametrize on 'request' or by passing count directly.
    Example: @pytest.mark.parametrize('existing_account_ids', [3], indirect=True)
    """
    count = getattr(request, 'param', 3)
    account_ids = []
    for _ in range(count):
        account_id = AccountIdPrimitivesMother.any()
        account = AccountMother.with_id(account_id)
        session.add(AccountModel.from_domain(account))
        account_ids.append(account_id)
    await session.commit()
    return account_ids


@pytest.fixture
async def existing_account_email(session: AsyncSession) -> str:
    email = AccountEmailPrimitivesMother.any()
    account = AccountMother.create(email=email)
    session.add(AccountModel.from_domain(account))
    await session.commit()
    return email
