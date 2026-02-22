from typing import override

from src.auth.account.domain.password_manager import PasswordManager


class FakePasswordManager(PasswordManager):
    def __init__(self) -> None:
        self._verification_result = None

    @override
    async def hash(self, plain_password: str) -> str:
        return plain_password

    @override
    async def verify_credentials(self, password: str) -> bool:
        return self._verification_result

    def should_verify(self, verification_result: bool) -> None:
        self._verification_result = verification_result
