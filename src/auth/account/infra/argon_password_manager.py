from typing import override

from argon2 import PasswordHasher

from src.auth.account.domain.password_manager import PasswordManager


class ArgonPasswordManager(PasswordManager):
    _hasher: PasswordHasher = PasswordHasher(
        time_cost=2,
        memory_cost=65536,
        parallelism=4,
    )

    @override
    def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)
