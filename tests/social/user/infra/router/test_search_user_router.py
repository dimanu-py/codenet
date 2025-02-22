import json

import pytest
from expects import expect, equal
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from src.delivery.api.main import app
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


@pytest.mark.acceptance
class TestSearchUserRouter:
    def setup_method(self) -> None:
        self._client = TestClient(app)

    @pytest.mark.asyncio
    async def test_should_search_user_based_on_filters(self) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(user_id, request_body)
        filters = [
            {"field": "username", "operator": "eq", "value": request_body["username"]}
        ]

        response = await self.when_a_get_request_is_made_to(
            "/users/search/", query_params={"filters": json.dumps(filters)}
        )

        expected_response = {"users": [{"id": user_id, **request_body}]}
        self.assert_response_satisfies(200, expected_response, response)

    async def given_a_user_is_signed_up(self, user_id: str, request_body: dict) -> None:
        with self._client as client:
            client.post(f"/users/signup/{user_id}", json=request_body)

    async def when_a_get_request_is_made_to(
        self, path: str, query_params: dict
    ) -> JSONResponse:
        with self._client as client:
            return client.get(path, params=query_params)  # type: ignore

    @staticmethod
    def assert_response_satisfies(
        expected_status_code: int, expected_response: dict, response: JSONResponse
    ) -> None:
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))
