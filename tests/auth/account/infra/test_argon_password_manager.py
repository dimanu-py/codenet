import pytest
from expects import equal, expect

from src.auth.account.infra.argon_password_manager import ArgonPasswordManager


@pytest.mark.integration
class TestArgonPasswordManager:
    def setup_method(self) -> None:
        self._password_manager = ArgonPasswordManager()

    def test_should_hash_plain_password(self) -> None:
        plain_password = "securePassword123!"

        hashed_password = self._password_manager.hash(plain_password)

        expect(hashed_password).to_not(equal(plain_password))
