import pytest
from expects import equal, expect, raise_error

from src.backoffice.user.domain.user_name import InvalidNameFormat, UserName


@pytest.mark.unit
class TestUserName:
    @pytest.mark.parametrize(
        "valid_name",
        [
            pytest.param("John Doe", id="simple_name"),
            pytest.param("María López", id="name_with_accents"),
            pytest.param("Jean-François", id="name_with_hyphen"),
            pytest.param("Anna O'Neill", id="name_with_apostrophe"),
            pytest.param("José Ángel Gutiérrez", id="name_with_multiple_accents"),
            pytest.param("Núria Martínez", id="spanish_name_with_accents"),
            pytest.param("Björn Müller", id="german_name_with_umlaut"),
        ],
    )
    def test_should_create_user_name_with_valid_format(self, valid_name: str) -> None:
        name = UserName(valid_name)

        expect(name.value).to(equal(valid_name))

    @pytest.mark.parametrize(
        "invalid_name",
        [
            pytest.param("User123", id="with_numbers"),
            pytest.param("John_Doe", id="with_underscore"),
            pytest.param("Name@With#Symbols", id="with_special_symbols"),
            pytest.param("123456", id="only_numbers"),
            pytest.param("User+", id="with_plus_sign"),
        ],
    )
    def test_should_raise_error_when_name_has_invalid_format(self, invalid_name: str) -> None:
        expect(lambda: UserName(invalid_name)).to(raise_error(InvalidNameFormat))
