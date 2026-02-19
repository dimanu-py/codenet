from abc import ABC, abstractmethod

from src.auth.account.domain.account import Account
from src.auth.account.domain.accounts import Accounts
from src.shared.domain.criteria.criteria import Criteria


class AccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def matching(self, criteria: Criteria) -> Accounts:
        raise NotImplementedError
