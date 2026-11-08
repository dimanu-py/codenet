import asyncio

import pytest
from expects import equal, expect, have_keys
from fastapi import Response
from httpx import AsyncClient
from pytest_bdd import given, scenarios, then, when

from src.auth.account.domain.account import AccountPrimitives
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_primitives_mother import AccountPrimitivesMother

pytestmark = [pytest.mark.acceptance]


scenarios("authenticate_session.feature")


@pytest.fixture
async def existing_account_for_authentication(add_to_database, existing_account: AccountPrimitives) -> dict[str, str]:
    return {"email": existing_account["email"], "plain_password": existing_account["password"]}


@given("I have a registered account with valid email and password", target_fixture="existing_account")
def signed_up_account(existing_account_for_authentication: dict[str, str]) -> dict:
    return existing_account_for_authentication


@given("I haven't registered an account", target_fixture="non_existing_account")
def non_existing_account() -> AccountPrimitives:
    return AccountPrimitivesMother.dummy()


@when("I attempt to authenticate with valid credentials", target_fixture="authenticate_response")
def authenticate_session_with_valid_credentials(client: AsyncClient, existing_account: AccountPrimitives) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            "/app/auth/sessions/login",
            data={
                "username": existing_account["email"],
                "password": existing_account["plain_password"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    )


@when("I attempt to authenticate with wrong credentials", target_fixture="authenticate_response")
def authenticate_session_with_invalid_credentials(client: AsyncClient) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            "/app/auth/sessions/login",
            data={
                "username": AccountEmailPrimitivesMother.any(),
                "password": "invalid_password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    )


@when("I attempt to authenticate with non existing account credentials", target_fixture="authenticate_response")
def authenticate_session_with_non_existing_account_credentials(
    client: AsyncClient, non_existing_account: dict
) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            "/app/auth/sessions/login",
            data={
                "username": non_existing_account["email"],
                "password": non_existing_account["password"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    )


@then("I should receive an authentication token")
def verify_token_has_been_produced(authenticate_response: Response) -> None:
    expect(authenticate_response.status_code).to(equal(200))
    expect(authenticate_response.json()["data"]).to(have_keys("access_token", "token_type"))


@then("I should receive an authentication error")
def verify_authentication_error(authenticate_response: Response) -> None:
    expect(authenticate_response.status_code).to(equal(401))
    expect(authenticate_response.json()).to(have_keys("error"))
