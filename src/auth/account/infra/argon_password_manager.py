from typing import override

from src.auth.account.domain.password_manager import PasswordManager


class ArgonPasswordManager(PasswordManager):
    @override
    def hash(self, plain_password: str) -> str:
        raise NotImplementedError