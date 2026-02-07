import asyncio

import pytest
from expects import equal, expect
from httpx import AsyncClient, Response
from pytest_bdd import given, scenarios, then, when

from tests.auth.account.domain.mothers.account_email_primitives_mother import AccountEmailPrimitivesMother
from tests.auth.account.domain.mothers.account_password_hash_primitives_mother import AccountPasswordHashPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother

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


@when("I submit the signup form", target_fixture="signup_response")
def submit_signup_form(client: AsyncClient, signup_form: dict, user_id: str) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.post(f"{_ROUTE_PATH}{user_id}", json=signup_form))


@then("I should have an account and a user profile created")
def verify_signup_success(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(202))
