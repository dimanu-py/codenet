import asyncio

import pytest
from expects import equal, expect
from fastapi import Response
from httpx import AsyncClient
from pytest_bdd import given, scenarios, then, when

from src.social.user.domain.user import User

pytestmark = [pytest.mark.acceptance]

scenarios("removal_user.feature")


_ROUTE_PATH = "/app/users/"


@given("I am an existing user", target_fixture="existing_user_username")
def existing_user_to_remove(existing_user: User) -> str:
    return existing_user.username.value


@when("I request to remove my account", target_fixture="removal_response")
def attempt_remove_existing_user(
    client: AsyncClient,
    existing_user_username: str,
) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.delete(f"{_ROUTE_PATH}{existing_user_username}"))


@when("I attempt to remove the account for non existing user", target_fixture="removal_response")
def attempt_remove_non_existing_user(client: AsyncClient, user_username: str) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.delete(f"{_ROUTE_PATH}{user_username}"))


@then("I should receive an error message indicating the user does not exist")
def verify_user_has_not_been_found(removal_response: Response) -> None:
    expect(removal_response.status_code).to(equal(404))


@then("my account should be successfully removed")
def verify_user_removal_successful(removal_response: Response) -> None:
    expect(removal_response.status_code).to(equal(202))
