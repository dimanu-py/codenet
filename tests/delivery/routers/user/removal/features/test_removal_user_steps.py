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


@given("I am an existing user", target_fixture="existing_user_id")
def existing_user_to_remove(existing_user: User) -> str:
    return existing_user.id.value


@when("I request to remove my account", target_fixture="removal_response")
def attempt_remove_existing_user(
    client: AsyncClient,
    existing_user_id: str,
) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.delete(f"{_ROUTE_PATH}{existing_user_id}"))


@when("I attempt to remove the account for non existing user", target_fixture="removal_response")
def attempt_remove_non_existing_user(client: AsyncClient, user_id: str) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.delete(f"{_ROUTE_PATH}{user_id}"))


@when("I attempt to remove the account with an invalid user id format", target_fixture="removal_response")
def attempt_remove_user_with_invalid_id_format(client: AsyncClient) -> Response:
    loop = asyncio.get_event_loop()
    invalid_user_id = "invalid-uuid-format"
    return loop.run_until_complete(client.delete(f"{_ROUTE_PATH}{invalid_user_id}"))


@then("I should receive an error message indicating the user does not exist")
def verify_user_has_not_been_found(removal_response: Response) -> None:
    expect(removal_response.status_code).to(equal(404))


@then("my account should be successfully removed")
def verify_user_removal_successful(removal_response: Response) -> None:
    expect(removal_response.status_code).to(equal(202))


@then("I should receive an error message indicating the user id format is invalid")
def verify_invalid_user_id_format_error(removal_response: Response) -> None:
    expect(removal_response.status_code).to(equal(422))
