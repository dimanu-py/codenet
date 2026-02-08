import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.account.infra.persistence.account_model import AccountModel
from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.persistence.user_model import UserModel
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.backoffice.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.fixture
def user_id() -> str:
    return UserIdPrimitivesMother.any()


@pytest.fixture
def user_username() -> str:
    return UserUsernamePrimitivesMother.any()


@pytest.fixture
async def existing_user(session: AsyncSession, existing_account_id: str) -> User:
    user = UserMother.with_id(existing_account_id)
    session.add(UserModel.from_domain(user))
    await session.commit()
    return user


@pytest.fixture
def create_user_with_account(session: AsyncSession):
    """Factory fixture to create users with their corresponding accounts.

    Usage:
        users = [create_user_with_account(username="john"), create_user_with_account(username="jane")]
    """
    async def _create(username: str | None = None, user_id: str | None = None) -> User:
        if username:
            user = UserMother.with_username(username)
        elif user_id:
            user = UserMother.with_id(user_id)
        elif username and user_id:
            user = UserMother.create(username=username, id=user_id)
        else:
            user = UserMother.any()

        user_primitives = user.to_primitives()
        account = AccountMother.with_id(user_primitives["id"])
        session.add(AccountModel.from_domain(account))
        session.add(UserModel.from_domain(user))
        return user

    return _create

