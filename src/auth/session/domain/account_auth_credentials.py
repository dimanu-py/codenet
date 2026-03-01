from typing import override

from src.auth.shared.domain.password_manager import PasswordManager


class AccountAuthCredentials:
    def __init__(self, account_id: str, password: str, status: str) -> None:
        self._account_id = account_id
        self._password = password
        self._status = status

    async def verify_password(self, password: str, password_manager: PasswordManager) -> bool:
        return await password_manager.verify_credentials(password, self._password)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AccountAuthCredentials):
            return False
        return (
            self._account_id == other._account_id
            and self._password == other._password
            and self._status == other._status
        )
