import pytest
from expects import equal, expect, raise_error

from src.auth.account.domain.account_email import InvalidEmailFormat, AccountEmail


@pytest.mark.unit
class TestAccountEmail:
    def test_should_create_email_with_valid_format(self) -> None:
        valid_email = "test.user@example.com"

        email = AccountEmail(valid_email)

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
    def test_should_raise_error_when_email_has_invalid_format(self, invalid_email: str) -> None:
        expect(lambda: AccountEmail(invalid_email)).to(raise_error(InvalidEmailFormat))
