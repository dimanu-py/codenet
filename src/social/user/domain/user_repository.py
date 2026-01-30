from abc import ABC, abstractmethod

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_username import UserUsername


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, username: UserUsername) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def matching(self, criteria: Criteria) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, username: UserUsername) -> None:
        raise NotImplementedError
