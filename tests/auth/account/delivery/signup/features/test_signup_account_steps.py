import asyncio

import pytest
from expects import equal, expect
from httpx import AsyncClient, Response
from pytest_bdd import given, scenarios, then, when

from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import AccountPasswordHashPrimitivesMother
from tests.backoffice.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.backoffice.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother

pytestmark = [pytest.mark.acceptance]

scenarios("signup_account.feature")

_ROUTE_PATH = "/app/auth/account/"


@given("I have filled in the signup form with valid information", target_fixture="signup_form")
def filled_signup_form() -> dict:
    return {
        "name": UserNamePrimitivesMother.any(),
        "username": UserUsernamePrimitivesMother.any(),
        "email": AccountEmailPrimitivesMother.any(),
        "password": AccountPasswordHashPrimitivesMother.any(),
    }


@given("I have filled in the signup form with a username that is already registered", target_fixture="signup_form")
async def filled_signup_form_with_existing_username(existing_username: str) -> dict:
    return {
        "name": UserNamePrimitivesMother.any(),
        "username": existing_username,
        "email": AccountEmailPrimitivesMother.any(),
        "password": AccountPasswordHashPrimitivesMother.any(),
    }


@given("I have filled in the signup form with an email that is already registered", target_fixture="signup_form")
async def filled_signup_form_with_existing_email(existing_account_email: str) -> dict:
    return {
        "name": UserNamePrimitivesMother.any(),
        "username": UserUsernamePrimitivesMother.any(),
        "email": existing_account_email,
        "password": AccountPasswordHashPrimitivesMother.any(),
    }


@when("I submit the signup form", target_fixture="signup_response")
def submit_signup_form(client: AsyncClient, signup_form: dict, user_id: str) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.post(f"{_ROUTE_PATH}{user_id}", json=signup_form))


@then("I should have an account and a user profile created")
def verify_signup_success(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(202))


@then("I should see an error message indicating the username is already in use")
def verify_username_already_in_use_error(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(409))


@then("I should see an error message indicating the email is already in use")
def verify_email_already_in_use_error(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(409))

