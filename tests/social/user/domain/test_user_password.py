import pytest
from expects import expect, equal

from src.social.user.domain.user_password import UserPassword


@pytest.mark.unit
class TestUserPassword:
    def test_should_store_hashed_password(self) -> None:
        plain_password = "securePassword123!"

        password = UserPassword.from_plain_text(plain_password)

        expect(password.value).to_not(equal(plain_password))
