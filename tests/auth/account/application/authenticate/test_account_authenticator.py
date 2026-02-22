import pytest
from expects import equal, expect

from src.auth.account.application.authenticate.account_authenticator import AccountAuthenticator, InvalidCredentials
from src.auth.account.domain.account import Account
from src.auth.account.infra.authentication_token import AuthenticationToken
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import (
    AccountPasswordHashPrimitivesMother,
)
from tests.auth.account.infra.fake_password_manager import FakePasswordManager
from tests.auth.account.infra.fake_token_issuer import FakeTokenIssuer
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.shared.expects.matchers import async_expect, raise_error


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountAuthenticator:
    _ANY_EMAIL = AccountEmailPrimitivesMother.any()
    _ANY_PASSWORD = AccountPasswordHashPrimitivesMother.any()
    _ANY_TOKEN = {"access_token": "ee9c873b-3ec4-4ece-8fe7-4eb8734cacde", "token_type": "bearer", "expires_in": 3600}

    def setup_method(self) -> None:
        self._repository = MockAccountRepository()
        self._password_manager = FakePasswordManager()
        self._token_issuer = FakeTokenIssuer(self._ANY_TOKEN)
        self._authenticator = AccountAuthenticator(
            repository=self._repository, password_manager=self._password_manager, token_issuer=self._token_issuer
        )

    async def test_should_authenticate_successfully_an_account_with_valid_credentials(self) -> None:
        self._should_find_signed_up_account_matching_criteria([AccountMother.create(password=self._ANY_PASSWORD)])

        issued_token = await self._authenticator.execute(identification=self._ANY_EMAIL, password=self._ANY_PASSWORD)

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))

    async def test_should_not_allow_to_authenticate_when_password_is_not_correct(self) -> None:
        self._should_find_signed_up_account_matching_criteria([AccountMother.create(password=self._ANY_PASSWORD)])

        await async_expect(
            lambda: self._authenticator.execute(identification=self._ANY_EMAIL, password="other_password")
        ).to(raise_error(InvalidCredentials))

    async def test_should_not_allow_to_authenticate_when_account_with_given_email_does_not_exist(self) -> None:
        self._should_not_find_account_matching_criteria()

        await async_expect(
            lambda: self._authenticator.execute(identification=self._ANY_EMAIL, password=self._ANY_PASSWORD)
        ).to(raise_error(InvalidCredentials))

    def _should_not_find_account_matching_criteria(self) -> None:
        self._repository.should_not_match_criteria()

    def _should_find_signed_up_account_matching_criteria(self, *accounts: list[Account]) -> None:
        self._repository.should_match_criteria_with_successive_calls(*accounts)
