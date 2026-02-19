from collections.abc import Callable, Coroutine
from typing import Any

import pytest

from src.backoffice.user.domain.user import User
from src.backoffice.user.infra.persistence.user_model import UserModel
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother


@pytest.fixture
async def existing_user(existing_account_id: str, add_to_database) -> User:
    user = UserMother.with_id(existing_account_id)
    await add_to_database(UserModel.from_domain(user))
    return user


@pytest.fixture
async def existing_username(existing_account_id: str, add_to_database) -> str:
    username = UserUsernamePrimitivesMother.any()
    user = UserMother.create(id=existing_account_id, username=username)
    await add_to_database(UserModel.from_domain(user))
    return username


@pytest.fixture
def create_users_with_usernames(
    existing_account_ids: list[str], add_to_database
) -> Callable[[list[str]], Coroutine[Any, Any, list[str]]]:
    """Factory fixture to create users with specific usernames.

    Creates users for each of the provided usernames, associating them with existing account IDs.
    Usage:
        usernames = await create_users_with_usernames(['john', 'jane', 'bob'])
    """

    async def _create(usernames: list[str]) -> list[str]:
        for account_id, username in zip(existing_account_ids, usernames, strict=True):
            user = UserMother.create(id=account_id, username=username)
            await add_to_database(UserModel.from_domain(user))
        return usernames

    return _create
