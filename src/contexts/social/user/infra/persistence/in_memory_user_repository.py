from typing import override

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _users: dict[str, User]

    def __init__(self) -> None:
        self._users = {}

    @override
    def save(self, user: User) -> None:
        self._users[user.id] = user

    @override
    def search(self, user_id: str) -> User | None:
        return self._users.get(user_id)
