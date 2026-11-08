import pytest
from expects import equal, expect, have_keys
from httpx import AsyncClient

from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother


@pytest.mark.acceptance
class TestAuthenticateSessionEndpoint:
    _ROUTE_PATH = "/app/auth/sessions"
    _AN_USERNAME = "username"
    _AN_EMAIL = "username.email@gmail.com"
    _A_PASSWORD = "password!"

    _response = None

    async def test_should_authenticate_account_with_valid_credentials(self, client: AsyncClient) -> None:
        await self._given_an_account_exists(client)
        await self._when_the_account_attempts_to_authenticate(client)
        self._then_a_token_should_be_issued()

    async def test_should_not_allow_to_authenticate_with_wrong_password(self, client: AsyncClient) -> None:
        await self._given_an_account_exists(client)
        await self._when_the_account_attempts_to_authenticate_with_wrong_password(client)
        self._then_invalid_credential_error_should_raise()

    async def test_should_fail_to_authenticate_non_existing_account(self, client: AsyncClient) -> None:
        await self._when_a_non_existing_account_attempts_to_authenticate(client)
        self._then_invalid_credential_error_should_raise()

    async def _given_an_account_exists(self, client: AsyncClient) -> None:
        account_id = AccountIdPrimitivesMother.any()
        await client.post(
            f"/app/auth/accounts/{account_id}",
            json={
                "username": self._AN_USERNAME,
                "email": self._AN_EMAIL,
                "password": self._A_PASSWORD,
            },
        )

    async def _when_the_account_attempts_to_authenticate(self, client: AsyncClient) -> None:
        await self._submit_authentication(
            client,
            authentication_form={
                "username": self._AN_USERNAME,
                "password": self._A_PASSWORD,
            },
        )

    async def _when_the_account_attempts_to_authenticate_with_wrong_password(self, client: AsyncClient) -> None:
        await self._submit_authentication(
            client,
            authentication_form={
                "username": self._AN_USERNAME,
                "password": "wrong-password",
            },
        )

    async def _when_a_non_existing_account_attempts_to_authenticate(self, client: AsyncClient) -> None:
        await self._submit_authentication(
            client,
            authentication_form={
                "username": self._AN_USERNAME,
                "password": self._A_PASSWORD,
            },
        )

    def _then_a_token_should_be_issued(self) -> None:
        expect(self._response.status_code).to(equal(200))
        expect(self._response.json()["data"]).to(have_keys("access_token", "token_type"))

    def _then_invalid_credential_error_should_raise(self) -> None:
        expect(self._response.status_code).to(equal(401))
        expect(self._response.json()).to(have_keys("error"))

    async def _submit_authentication(self, client: AsyncClient, *, authentication_form: dict) -> None:
        self._response = await client.post(
            f"{self._ROUTE_PATH}/login",
            data=authentication_form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
