from abc import ABC, abstractmethod

from src.contexts.social.user.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError