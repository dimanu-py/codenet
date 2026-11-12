import pytest
from expects import equal, expect

from src.auth.session.application.session_authenticator import InvalidCredentials, SessionAuthenticator
from src.auth.session.infra.authentication_token import AuthenticationToken
from tests.auth.account.domain.mothers.account_primitives_mother import AccountPrimitivesMother
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.auth.session.infra.fake_token_issuer import FakeTokenIssuer
from tests.auth.session.infra.service.mock_account_credentials_finder import MockAccountCredentialsFinder
from tests.auth.shared.infra.fake_password_manager import FakePasswordManager
from tests.shared.expects.matchers import async_expect, raise_error


@pytest.mark.unit
@pytest.mark.asyncio
class TestSessionAuthenticator:
    _EXISTING_ACCOUNT = AccountPrimitivesMother.dummy()
    _ANY_TOKEN = {"access_token": "ee9c873b-3ec4-4ece-8fe7-4eb8734cacde", "token_type": "bearer", "expires_in": 3600}

    def setup_method(self) -> None:
        self._credentials_finder = MockAccountCredentialsFinder()
        self._password_manager = FakePasswordManager()
        self._token_issuer = FakeTokenIssuer(self._ANY_TOKEN)
        self._account_repository = MockAccountRepository()
        self._authenticator = SessionAuthenticator(
            credentials_finder=self._credentials_finder,
            password_verifier=self._password_manager,
            token_issuer=self._token_issuer,
            account_repository=self._account_repository,
        )

    @pytest.mark.parametrize(
        "identification",
        [
            pytest.param(_EXISTING_ACCOUNT["email"], id="identified_with_email"),
            pytest.param(_EXISTING_ACCOUNT["username"], id="identified_with_username"),
        ],
    )
    async def test_should_authenticate_successfully_an_account_with_valid_credentials(
        self, identification: str
    ) -> None:
        self._should_find_signed_up_account()

        issued_token = await self._authenticator.execute(
            identification=identification, password=self._EXISTING_ACCOUNT["password"]
        )

        expect(issued_token).to(equal(AuthenticationToken(**self._ANY_TOKEN)))

    async def test_should_issue_token_using_account_id_instead_of_login_identification(self) -> None:
        self._should_find_signed_up_account()

        await self._authenticator.execute(
            identification=self._EXISTING_ACCOUNT["email"], password=self._EXISTING_ACCOUNT["password"]
        )

        expect(self._token_issuer.received_account_id).to(equal(self._EXISTING_ACCOUNT["id"]))

    async def test_should_not_allow_to_authenticate_when_password_is_not_correct(self) -> None:
        self._should_find_signed_up_account()
        wrong_password = "a-different-password"

        await async_expect(
            lambda: self._authenticator.execute(identification=self._EXISTING_ACCOUNT["email"], password=wrong_password)
        ).to(raise_error(InvalidCredentials))

    async def test_should_not_allow_to_authenticate_when_account_with_given_email_is_not_signed_up(self) -> None:
        self._should_not_find_signed_up_account()

        await async_expect(
            lambda: self._authenticator.execute(
                identification=self._EXISTING_ACCOUNT["email"], password=self._EXISTING_ACCOUNT["password"]
            )
        ).to(raise_error(InvalidCredentials))

    def _should_not_find_signed_up_account(self) -> None:
        self._account_repository.should_not_match_criteria()

    def _should_find_signed_up_account(self) -> None:
        self._account_repository.should_match_criteria_with_successive_calls(self._EXISTING_ACCOUNT)
