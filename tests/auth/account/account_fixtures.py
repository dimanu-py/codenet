import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.account.domain.account import Account
from src.auth.account.infra.persistence.account_model import AccountModel
from tests.auth.account.domain.mothers.account_mother import AccountMother


@pytest.fixture
async def existing_account(session: AsyncSession) -> Account:
    account = AccountMother.any()
    session.add(AccountModel.from_domain(account))
    await session.commit()
    return account
