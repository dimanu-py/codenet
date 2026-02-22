from abc import ABC, abstractmethod


class PasswordManager(ABC):
    @abstractmethod
    async def hash(self, plain_password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_credentials(self, password: str, stored_password: str) -> bool:
        raise NotImplementedError
