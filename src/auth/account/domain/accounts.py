from collections.abc import Iterable
from typing import Self

from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email import AccountEmail
from src.auth.account.domain.account_username import AccountUsername


class Accounts:
    def __init__(self, accounts: list[Account]) -> None:
        self._accounts = accounts

    def has_accounts(self) -> bool:
        return len(self._accounts) > 0

    def has_email(self, email: str) -> bool:
        return any(account.has_email(AccountEmail(email)) for account in self._accounts)

    def has_username(self, username: str) -> bool:
        return any(account.has_username(AccountUsername(username)) for account in self._accounts)

    def first(self) -> Account:
        return self._accounts[0]

    def __iter__(self) -> Iterable[Account]:
        return iter(self._accounts)

    def __len__(self) -> int:
        return len(self._accounts)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Accounts):
            return False
        return self._accounts == other._accounts
