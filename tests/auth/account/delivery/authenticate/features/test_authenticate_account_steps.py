import asyncio

import pytest
from expects import expect, equal, have_keys
from fastapi import Response
from httpx import AsyncClient
from pytest_bdd import scenarios, given, when, then

from src.auth.account.domain.account import Account
from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_mother import AccountMother

pytestmark = [pytest.mark.acceptance]


scenarios("authenticate_account.feature")

_ROUTE_PATH = "/app/auth/accounts/login"


@given("I have a registered account with valid email and password", target_fixture="existing_account")
def signed_up_account(existing_account: Account) -> dict:
    return existing_account.to_primitives()


@given("I haven't registered an account", target_fixture="non_existing_account")
def non_existing_account() -> dict:
    return AccountMother.any().to_primitives()


@when("I attempt to authenticate with valid credentials", target_fixture="authenticate_response")
def authenticate_account_with_valid_credentials(client: AsyncClient, existing_account: dict) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            _ROUTE_PATH,
            data={
                "username": existing_account["email"],
                "password": existing_account["password"],
            },
        )
    )


@when("I attempt to authenticate with wrong credentials", target_fixture="authenticate_response")
def authenticate_account_with_invalid_credentials(client: AsyncClient) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            _ROUTE_PATH,
            data={
                "username": AccountEmailPrimitivesMother.any(),
                "password": "invalid_password",
            },
        )
    )


@when("I attempt to authenticate with non existing account credentials", target_fixture="authenticate_response")
def authenticate_account_with_non_existing_account_credentials(client: AsyncClient, non_existing_account: dict) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        client.post(
            _ROUTE_PATH,
            data={
                "username": non_existing_account["email"],
                "password": non_existing_account["password"],
            },
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
