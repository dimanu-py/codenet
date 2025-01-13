from abc import ABC, abstractmethod

from src.contexts.social.user.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        raise NotImplementedError
