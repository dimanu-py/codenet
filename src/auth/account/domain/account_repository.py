from abc import ABC, abstractmethod

from src.auth.account.domain.account import Account


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None:
        raise NotImplementedError
