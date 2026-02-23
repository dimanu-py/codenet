from typing import override

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError

from src.auth.account.domain.password_manager import PasswordManager


class ArgonPasswordManager(PasswordManager):
    _hasher: PasswordHasher = PasswordHasher(
        time_cost=2,
        memory_cost=65536,
        parallelism=4,
    )

    @override
    async def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    @override
    async def verify_credentials(self, password: str, stored_password: str) -> bool:
        try:
            return self._hasher.verify(stored_password, password)
        except InvalidHashError:
            return False
