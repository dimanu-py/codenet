from abc import ABC, abstractmethod

from src.contexts.social.user.domain.user import User
from src.contexts.social.user.domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        raise NotImplementedError
