from typing import override

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _users: dict[str, User]

    def __init__(self) -> None:
        self._users = {}

    @override
    async def save(self, user: User) -> None:
        self._users[user.id] = user

    @override
    async def search(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    @override
    async def delete(self, user_id: str) -> None:
        del self._users[user_id]
