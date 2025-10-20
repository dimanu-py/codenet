import ast
import asyncio
import json

import pytest
from expects import expect, equal, contain, have_length
from fastapi import Response
from httpx import AsyncClient
from pytest_bdd import scenarios, given, when, parsers, then
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.social.user.infra.persistence.user_model import UserModel
from tests.social.user.domain.mothers.user_mother import UserMother

pytestmark = [pytest.mark.acceptance]

scenarios("search_user.feature")


_ROUTE_PATH = "/app/users/"


@given(parsers.parse("there are users with usernames {usernames}"))
def existing_users(session: AsyncSession, usernames: str) -> None:
    usernames = ast.literal_eval(usernames)
    users = [UserMother.with_username(username) for username in usernames]
    for user in users:
        session.add(UserModel(**user.to_primitives()))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(session.commit())


@when(parsers.parse('I search for users with username "{username}"'), target_fixture="search_response")
def search_users_by_username(client: AsyncClient, username: str) -> Response:
    filters = {
        "field": "username",
        "contains": username
    }
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.get(_ROUTE_PATH, params={"filter": json.dumps(filters)}))


@then(parsers.parse('I should see the users with username "{username}"'))
def verify_users_found_by_username(search_response: Response, username: str) -> None:
    expect(search_response.status_code).to(equal(200))
    users = search_response.json()["users"]
    expect(users).to(have_length(2))
    for user in users:
        expect(user["username"]).to(contain(username))
