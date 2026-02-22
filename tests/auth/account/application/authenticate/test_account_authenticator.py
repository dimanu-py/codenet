import pytest
from expects import equal, expect

from src.auth.account.application.authenticate.account_authenticator import AccountAuthenticator
from src.auth.account.infra.authentication_token import AuthenticationToken
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.infra.fake_password_manager import FakePasswordManager
from tests.auth.account.infra.fake_token_issuer import FakeTokenIssuer


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountAuthenticator:
    _ANY_EMAIL = AccountEmailPrimitivesMother.any()
    _ANY_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _ANY_TOKEN = {"access_token": "ee9c873b-3ec4-4ece-8fe7-4eb8734cacde", "token_type": "bearer", "expires_in": 3600}

    def setup_method(self) -> None:
        self._password_manager = FakePasswordManager()
        self._token_issuer = FakeTokenIssuer(self._ANY_TOKEN)
        self._authenticator = AccountAuthenticator(password_manager=self._password_manager, token_issuer=self._token_issuer)

    async def test_should_authenticate_successfully_an_account_with_valid_credentials(self) -> None:
        issued_token = await self._authenticator.execute(identification=self._ANY_EMAIL, password=self._ANY_PASSWORD)

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))
