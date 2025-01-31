from abc import ABC, abstractmethod

from src.social.user.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError
