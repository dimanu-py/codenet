from typing import Callable, Any, Coroutine

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.persistence.user_model import UserModel
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.fixture
async def existing_user(session: AsyncSession, existing_account_id: str) -> User:
    user = UserMother.with_id(existing_account_id)
    session.add(UserModel.from_domain(user))
    await session.commit()
    return user


@pytest.fixture
async def existing_username(session: AsyncSession, existing_account_id: str) -> str:
    username = UserUsernamePrimitivesMother.any()
    user = UserMother.create(id=existing_account_id, username=username)
    session.add(UserModel.from_domain(user))
    await session.commit()
    return username


@pytest.fixture
def create_users_with_usernames(
    session: AsyncSession, existing_account_ids: list[str]
) -> Callable[[list[str]], Coroutine[Any, Any, list[str]]]:
    """Factory fixture to create users with specific usernames.

    Creates users for each of the provided usernames, associating them with existing account IDs.
    Usage:
        usernames = await create_users_with_usernames(['john', 'jane', 'bob'])
    """

    async def _create(usernames: list[str]) -> list[str]:
        for account_id, username in zip(existing_account_ids, usernames):
            user = UserMother.create(id=account_id, username=username)
            session.add(UserModel.from_domain(user))
        await session.commit()
        return usernames

    return _create
