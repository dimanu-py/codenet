from src.auth.account.domain.password_manager import PasswordManager


class FakePasswordManager(PasswordManager):
    def hash(self, plain_password: str) -> str:
        return plain_password