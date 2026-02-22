from typing import override

from src.auth.account.domain.password_manager import PasswordManager


class FakePasswordManager(PasswordManager):
    @override
    async def hash(self, plain_password: str) -> str:
        return plain_password

    @override
    async def verify_credentials(self, password: str) -> bool:
        raise NotImplementedError
