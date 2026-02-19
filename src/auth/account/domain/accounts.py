from collections.abc import Iterable
from typing import Self

from src.auth.account.domain.account import Account


class Accounts:
    def __init__(self, accounts: list[Account]) -> None:
        self._accounts = accounts

    def __iter__(self)-> Iterable[Account]:
        return iter(self._accounts)

    def __len__(self) -> int:
        return len(self._accounts)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Accounts):
            return False
        return self._accounts == other._accounts