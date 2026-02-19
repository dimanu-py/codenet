from src.auth.account.domain.account import Account


class Accounts:
    def __init__(self, accounts: list[Account]) -> None:
        self._accounts = accounts
