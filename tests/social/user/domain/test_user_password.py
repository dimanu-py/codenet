import pytest
from expects import expect, equal, raise_error

from src.social.user.domain.user_password import UserPassword, CannotStorePlainTextPassword


@pytest.mark.unit
class TestUserPassword:
    def test_should_store_hashed_password(self) -> None:
        plain_password = "securePassword123!"

        password = UserPassword.from_plain_text(plain_password)

        expect(password.value).to_not(equal(plain_password))

    def test_should_raise_error_when_trying_to_store_not_hashed_password(self) -> None:
        plain_password = "securePassword123!"

        expect(lambda: UserPassword(plain_password)).to(raise_error(CannotStorePlainTextPassword))

