from abc import ABC, abstractmethod


class PasswordManager(ABC):
    @abstractmethod
    async def hash(self, plain_password: str) -> str:
        raise NotImplementedError
