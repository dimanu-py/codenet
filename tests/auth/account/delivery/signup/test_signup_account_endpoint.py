import pytest
from expects import equal, expect
from httpx import AsyncClient

from tests.auth.account.domain.mothers.account_id_primitives_mother import AccountIdPrimitivesMother


@pytest.mark.acceptance
class TestSignupAccountEndpoint:
    _ROUTE_PATH = "/app/auth/accounts"
    _AN_USERNAME = "username"
    _AN_EMAIL = "username.email@gmail.com"
    _A_SIGNUP_FORM = {
        "username": _AN_USERNAME,
        "email": _AN_EMAIL,
        "password": "password!",
    }
    _response = None

    async def test_should_signup_account_successfully(self, client: AsyncClient) -> None:
        await self._when_a_new_signup_up_form_is_submitted(client)
        self._then_a_new_account_is_signed_up()

    async def test_should_not_allow_to_sign_up_a_registered_email(self, client: AsyncClient) -> None:
        await self._given_an_existing_account(client)
        await self._when_a_new_signup_form_is_submitted_with_the_same_email(client)
        self._then_registered_email_error_should_raise()

    async def test_should_not_allo_to_sign_up_a_registered_username(self, client: AsyncClient) -> None:
        await self._given_an_existing_account(client)
        await self._when_a_new_signup_form_is_submitted_with_the_same_username(client)
        self._then_registered_username_error_should_raise()

    async def _given_an_existing_account(self, client: AsyncClient) -> None:
        await self._submit_signup_form(
            client,
            signup_data=self._A_SIGNUP_FORM,
        )

    async def _when_a_new_signup_up_form_is_submitted(self, client: AsyncClient) -> None:
        await self._submit_signup_form(
            client,
            signup_data=self._A_SIGNUP_FORM,
        )

    async def _when_a_new_signup_form_is_submitted_with_the_same_email(self, client: AsyncClient) -> None:
        await self._submit_signup_form(
            client,
            signup_data={
                "username": "different.username",
                "email": self._AN_EMAIL,
                "password": "password!",
            },
        )

    async def _when_a_new_signup_form_is_submitted_with_the_same_username(self, client: AsyncClient) -> None:
        await self._submit_signup_form(
            client,
            signup_data={
                "username": self._AN_USERNAME,
                "email": "different.email@gmail.com",
                "password": "password!",
            },
        )

    def _then_a_new_account_is_signed_up(self) -> None:
        expect(self._response.status_code).to(equal(202))

    def _then_registered_email_error_should_raise(self) -> None:
        expect(self._response.status_code).to(equal(409))

    def _then_registered_username_error_should_raise(self) -> None:
        expect(self._response.status_code).to(equal(409))

    async def _submit_signup_form(self, client: AsyncClient, *, signup_data: dict) -> None:
        account_id = AccountIdPrimitivesMother.any()
        self._response = await client.post(
            f"{self._ROUTE_PATH}/{account_id}",
            json=signup_data,
        )
