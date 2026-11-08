from typing import override

from src.auth.shared.domain.password_manager import PasswordManager


class AccountAuthCredentials:
    def __init__(self, account_id: str, password: str) -> None:
        self._account_id = account_id
        self._password = password

    @property
    def account_id(self) -> str:
        return self._account_id

    async def password_is_incorrect(self, password: str, password_manager: PasswordManager) -> bool:
        return not await password_manager.verify_credentials(password, self._password)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AccountAuthCredentials):
            return False
        return self._account_id == other._account_id and self._password == other._password
