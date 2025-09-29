import pytest
from expects import expect, equal, raise_error

from src.social.user.domain.user_email import UserEmail, InvalidEmailFormatError


@pytest.mark.unit
class TestUserEmail:
    def test_should_create_user_email_with_valid_format(self) -> None:
        valid_email = "test.user@example.com"

        email = UserEmail(valid_email)

        expect(email.value).to(equal(valid_email))

    @pytest.mark.parametrize(
        "invalid_email",
        [
            pytest.param("invalid-email", id="missing_at_and_domain"),
            pytest.param("no-at-sign.example.com", id="missing_at_symbol"),
            pytest.param("@no-local-part.com", id="missing_local_part"),
            pytest.param("no-domain@", id="missing_domain"),
            pytest.param("spaces in@email.com", id="contains_spaces"),
            pytest.param("special#chars@email.com", id="contains_special_chars"),
        ],
    )
    def test_should_raise_error_when_email_has_invalid_format(
        self, invalid_email: str
    ) -> None:
        expect(lambda: UserEmail(invalid_email)).to(
            raise_error(InvalidEmailFormatError)
        )
