import pytest
from expects import expect, equal, be_true
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.session.domain.account_auth_credentials import AccountAuthCredentials
from src.auth.session.domain.login_identifier import LoginIdentifier
from src.auth.session.infra.service.postgres_account_credentials_finder import PostgresAccountCredentialsFinder


@pytest.mark.integration
@pytest.mark.asyncio
class TestPostgresAccountCredentialsFinder:
    @pytest.fixture(autouse=True)
    def setup_method(self, session: AsyncSession) -> None:
        self._session = session
        self._credentials_finder = PostgresAccountCredentialsFinder(session)

    async def test_should_return_account_credentials_of_an_existing_account_using_email(self, existing_account) -> None:
        account_primitives = existing_account.to_primitives()
        login_identifier = LoginIdentifier(account_primitives["email"])

        account_auth_credentials = await self._credentials_finder.find_by_login_identifier(login_identifier)

        expect(account_auth_credentials.is_present()).to(be_true)
        expect(account_auth_credentials.unwrap()).to(
            equal(
                AccountAuthCredentials(
                    account_id=account_primitives["id"],
                    password=account_primitives["password"],
                    status=account_primitives["status"],
                )
            )
        )

    async def test_should_return_account_credentials_of_an_existing_account_using_username(
        self, existing_account
    ) -> None:
        account_primitives = existing_account.to_primitives()
        login_identifier = LoginIdentifier(account_primitives["username"])

        account_auth_credentials = await self._credentials_finder.find_by_login_identifier(login_identifier)

        expect(account_auth_credentials.is_present()).to(be_true)
        expect(account_auth_credentials.unwrap()).to(
            equal(
                AccountAuthCredentials(
                    account_id=account_primitives["id"],
                    password=account_primitives["password"],
                    status=account_primitives["status"],
                )
            )
        )

    @pytest.mark.parametrize(
        "login_identifier",
        [
            pytest.param(LoginIdentifier("non-existing-email"), id="using_email"),
            pytest.param(LoginIdentifier("non-existing-username"), id="using_username"),
        ],
    )
    async def test_should_return_none_when_account_with_given_login_identifier_is_not_signed_up(
        self, login_identifier: LoginIdentifier
    ) -> None:
        account_auth_credentials = await self._credentials_finder.find_by_login_identifier(login_identifier)

        expect(account_auth_credentials.is_empty()).to(be_true)
