import pytest
from expects import equal, expect

from src.auth.session.application.authenticate.session_authenticator import InvalidCredentials, SessionAuthenticator
from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.infra.authentication_token import AuthenticationToken
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.domain.mothers.account_username_primitives_mother import AccountUsernamePrimitivesMother
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.auth.session.domain.mothers.account_auth_credentials_mother import AccountAuthCredentialsMother
from tests.auth.session.infra.fake_token_issuer import FakeTokenIssuer
from tests.auth.session.infra.service.mock_account_credentials_finder import MockAccountCredentialsFinder
from tests.auth.shared.infra.fake_password_manager import FakePasswordManager
from tests.shared.expects.matchers import async_expect, raise_error


@pytest.mark.unit
@pytest.mark.asyncio
class TestSessionAuthenticator:
    _EXISTING_EMAIL = AccountEmailPrimitivesMother.any()
    _EXISTING_USERNAME = AccountUsernamePrimitivesMother.any()
    _EXISTING_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _SIGNED_UP_ACCOUNT_AUTH_CREDENTIALS = AccountAuthCredentialsMother.with_password(_EXISTING_PASSWORD)
    _ANY_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _ANY_TOKEN = {"access_token": "ee9c873b-3ec4-4ece-8fe7-4eb8734cacde", "token_type": "bearer", "expires_in": 3600}

    def setup_method(self) -> None:
        self._repository = MockAccountRepository()
        self._credentials_finder = MockAccountCredentialsFinder()
        self._password_manager = FakePasswordManager()
        self._token_issuer = FakeTokenIssuer(self._ANY_TOKEN)
        self._authenticator = SessionAuthenticator(credentials_finder=self._credentials_finder, password_verifier=self._password_manager,
                                                   token_issuer=self._token_issuer)

    async def test_should_authenticate_successfully_an_account_with_valid_credentials(self) -> None:
        self._should_find_signed_up_account_auth_credentials(self._SIGNED_UP_ACCOUNT_AUTH_CREDENTIALS)

        issued_token = await self._authenticator.execute(
            identification=self._EXISTING_EMAIL, password=self._EXISTING_PASSWORD
        )

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))

    async def test_should_not_allow_to_authenticate_when_password_is_not_correct(self) -> None:
        self._should_find_signed_up_account_auth_credentials(self._SIGNED_UP_ACCOUNT_AUTH_CREDENTIALS)

        await async_expect(
            lambda: self._authenticator.execute(identification=self._EXISTING_EMAIL, password=self._ANY_PASSWORD)
        ).to(raise_error(InvalidCredentials))

    async def test_should_not_allow_to_authenticate_when_account_with_given_email_is_not_signed_up(self) -> None:
        self._should_not_find_account_auth_credentials()

        await async_expect(
            lambda: self._authenticator.execute(identification=self._EXISTING_EMAIL, password=self._EXISTING_PASSWORD)
        ).to(raise_error(InvalidCredentials))

    async def test_should_authenticate_successfully_an_account_with_valid_username(self) -> None:
        self._should_find_signed_up_account_auth_credentials(self._SIGNED_UP_ACCOUNT_AUTH_CREDENTIALS)

        issued_token = await self._authenticator.execute(
            identification=self._EXISTING_USERNAME, password=self._EXISTING_PASSWORD
        )

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))

    def _should_not_find_account_auth_credentials(self) -> None:
        self._credentials_finder.should_search_and_not_find_account_auth_credentials()

    def _should_find_signed_up_account_auth_credentials(self, account_auth_credentials: AccountAuthCredentials) -> None:
        self._credentials_finder.should_search_and_find(account_auth_credentials)
