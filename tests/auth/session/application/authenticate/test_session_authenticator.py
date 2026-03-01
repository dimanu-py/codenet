import pytest
from expects import equal, expect

from src.auth.session.application.authenticate.session_authenticator import InvalidCredentials, SessionAuthenticator
from src.auth.session.infra.authentication_token import AuthenticationToken
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.domain.mothers.account_username_primitives_mother import AccountUsernamePrimitivesMother
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.auth.session.infra.fake_token_issuer import FakeTokenIssuer
from tests.auth.session.infra.service.mock_account_credentials_finder import MockAccountCredentialsFinder
from tests.auth.shared.infra.fake_password_manager import FakePasswordManager
from tests.shared.expects.matchers import async_expect, raise_error


@pytest.mark.unit
@pytest.mark.asyncio
class TestSessionAuthenticator:
    _EXISTING_EMAIL = AccountEmailPrimitivesMother.any()
    _EXISTING_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _SIGNED_UP_ACCOUNT = AccountMother.create(email=_EXISTING_EMAIL, password=_EXISTING_PASSWORD)
    _ANY_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _ANY_TOKEN = {"access_token": "ee9c873b-3ec4-4ece-8fe7-4eb8734cacde", "token_type": "bearer", "expires_in": 3600}

    def setup_method(self) -> None:
        self._repository = MockAccountRepository()
        self._credentials_finder = MockAccountCredentialsFinder()
        self._password_manager = FakePasswordManager()
        self._token_issuer = FakeTokenIssuer(self._ANY_TOKEN)
        self._authenticator = SessionAuthenticator(
            repository=self._repository, password_verifier=self._password_manager, token_issuer=self._token_issuer
        )

    async def test_should_authenticate_successfully_an_account_with_valid_credentials(self) -> None:
        self._should_find_signed_up_account_matching_criteria([self._SIGNED_UP_ACCOUNT])

        issued_token = await self._authenticator.execute(
            identification=self._EXISTING_EMAIL, password=self._EXISTING_PASSWORD
        )

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))

    async def test_should_not_allow_to_authenticate_when_password_is_not_correct(self) -> None:
        self._should_find_signed_up_account_matching_criteria([self._SIGNED_UP_ACCOUNT])

        await async_expect(
            lambda: self._authenticator.execute(identification=self._EXISTING_EMAIL, password=self._ANY_PASSWORD)
        ).to(raise_error(InvalidCredentials))

    async def test_should_not_allow_to_authenticate_when_account_with_given_email_is_not_signed_up(self) -> None:
        self._should_not_find_account_matching_criteria()

        await async_expect(
            lambda: self._authenticator.execute(identification=self._EXISTING_EMAIL, password=self._EXISTING_PASSWORD)
        ).to(raise_error(InvalidCredentials))

    def _should_not_find_account_matching_criteria(self) -> None:
        self._repository.should_not_match_criteria()

    def _should_find_signed_up_account_matching_criteria(self, *accounts: list) -> None:
        self._repository.should_match_criteria_with_successive_calls(*accounts)

    async def test_should_authenticate_successfully_an_account_with_valid_username(self) -> None:
        existing_username = AccountUsernamePrimitivesMother.any()
        signed_up_account = AccountMother.create(
            username=existing_username, email=self._EXISTING_EMAIL, password=self._EXISTING_PASSWORD
        )
        self._should_find_signed_up_account_matching_criteria([signed_up_account])

        issued_token = await self._authenticator.execute(
            identification=existing_username, password=self._EXISTING_PASSWORD
        )

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))
