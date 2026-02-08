from abc import ABC, abstractmethod

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmail
from src.shared.domain.value_objects.optional import Optional


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search_by_email(self, email: AccountEmail) -> Optional[Account]:
        raise NotImplementedError
