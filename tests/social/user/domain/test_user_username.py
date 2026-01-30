import pytest
from expects import equal, expect, raise_error

from src.social.user.domain.user_username import (
    InvalidUsernameFormat,
    UserUsername,
)


@pytest.mark.unit
class TestUserUsername:
    @pytest.mark.parametrize(
        "valid_username",
        [
            pytest.param("user123", id="alphanumeric"),
            pytest.param("john_doe", id="with_underscore"),
            pytest.param("alice.smith", id="with_period"),
            pytest.param("developer42", id="alphanumeric_with_numbers"),
            pytest.param("tech_guru", id="with_underscore_words"),
        ],
    )
    def test_should_create_user_username_with_valid_format(self, valid_username: str) -> None:
        username = UserUsername(valid_username)

        expect(username.value).to(equal(valid_username))

    @pytest.mark.parametrize(
        "invalid_username",
        [
            pytest.param("user-name", id="with_hyphen"),
            pytest.param("user name", id="with_space"),
            pytest.param("special@chars", id="with_at_symbol"),
            pytest.param("español", id="with_non_ascii"),
            pytest.param("user#123", id="with_hash_symbol"),
            pytest.param("john$doe", id="with_dollar_symbol"),
        ],
    )
    def test_should_raise_error_when_username_has_invalid_format(self, invalid_username: str) -> None:
        expect(lambda: UserUsername(invalid_username)).to(raise_error(InvalidUsernameFormat))
