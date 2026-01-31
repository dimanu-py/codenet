import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.social.user.domain.user import User
from src.social.user.infra.persistence.user_model import UserModel
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_mother import UserMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.fixture
def user_id() -> str:
    return UserIdPrimitivesMother.any()


@pytest.fixture
def user_username() -> str:
    return UserUsernamePrimitivesMother.any()


@pytest.fixture
async def existing_user(session: AsyncSession) -> User:
    user = UserMother.any()
    session.add(UserModel.from_domain(user))
    await session.commit()
    return user
