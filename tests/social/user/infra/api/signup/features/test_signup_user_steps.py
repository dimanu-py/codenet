import asyncio

import pytest
from expects import equal, expect
from httpx import AsyncClient, Response
from pytest_bdd import given, scenarios, then, when

from tests.social.user.domain.mothers.user_email_mother import UserEmailMother
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.domain.mothers.user_name_mother import UserNameMother
from tests.social.user.domain.mothers.user_username_mother import UserUsernameMother

pytestmark = [pytest.mark.acceptance]

scenarios("signup_user.feature")

_ROUTE_PATH = "/app/users/"


@pytest.fixture
def user_id() -> str:
    return UserIdMother.any().value


@given("I have filled a signup form with valid details", target_fixture="signup_form")
def filled_signup_form() -> dict:
    return {
        "name": UserNameMother.any().value,
        "username": UserUsernameMother.any().value,
        "email": UserEmailMother.any().value,
    }


@given("the user id does not conform to the required format", target_fixture="user_id")
def invalid_user_id() -> str:
    return "invalid-uuid-format"


@when("I submit the signup form", target_fixture="signup_response")
def submit_signup_form(client: AsyncClient, signup_form: dict, user_id: str) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.post(f"{_ROUTE_PATH}{user_id}", json=signup_form))


@then("I should be signed up successfully")
def verify_signup_success(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(201))


@then("I should see an error message indicating invalid user id format")
def verify_signup_failure_invalid_name(signup_response: Response) -> None:
    expect(signup_response.status_code).to(equal(422))
