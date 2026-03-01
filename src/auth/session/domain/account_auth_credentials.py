from src.auth.shared.domain.password_manager import PasswordManager


class AccountAuthCredentials:
    def __init__(self, account_id: str, password: str, status: str) -> None:
        self._account_id = account_id
        self._password = password
        self._status = status

    async def verify_password(self, password: str, password_manager: PasswordManager) -> bool:
        return await password_manager.verify_credentials(password, self._password)
