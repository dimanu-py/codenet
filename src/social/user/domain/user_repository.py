from abc import ABC, abstractmethod

from src.shared.domain.criteria.criteria import Criteria
from src.social.user.domain.user import User
from src.social.user.domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def matching(self, criteria: Criteria) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        raise NotImplementedError
