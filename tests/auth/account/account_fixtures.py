import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.infra.persistence.account_model import AccountModel
from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother


@pytest.fixture
async def existing_account_id(session: AsyncSession) -> str:
    account_id = AccountIdPrimitivesMother.any()
    account = AccountMother.with_id(account_id)
    session.add(AccountModel.from_domain(account))
    await session.commit()
    return account_id
