import pytest
from expects import expect, equal, raise_error, be_true, be_false

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

    def test_should_return_true_when_password_matches_stored_value(self) -> None:
        plain_password = "securePassword123!"
        stored_password = UserPassword.from_plain_text(plain_password)

        password_matches = stored_password.verify(plain_password)

        expect(password_matches).to(be_true)

    def test_should_return_false_when_password_does_not_match_stored_value(self) -> None:
        plain_password = "securePassword123!"
        stored_password = UserPassword.from_plain_text(plain_password)
        wrong_password = "wrongPassword456!"

        password_matches = stored_password.verify(wrong_password)

        expect(password_matches).to(be_false)
