import pytest

from src.auth.account.domain.account import AccountPrimitives
from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.persistence.user_model import UserModel
from tests.backoffice.user.domain.mothers.user_mother import UserMother


@pytest.fixture
async def existing_user(existing_account: AccountPrimitives, add_to_database) -> User:
    user = UserMother.with_id(existing_account["id"])
    await add_to_database(UserModel.from_domain(user))
    return user
