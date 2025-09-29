import pytest
from expects import expect, equal
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse

from src.delivery.main import app
from tests.social.user.domain.mother.user_email_mother import UserEmailMother
from tests.social.user.domain.mother.user_id_mother import UserIdMother
from tests.social.user.domain.mother.user_name_mother import UserNameMother
from tests.social.user.domain.mother.user_username_mother import UserUsernameMother


@pytest.mark.acceptance
@pytest.mark.asyncio
class UserModuleAcceptanceTestConfig:
    EMPTY_RESPONSE: dict = {}

    def setup_method(self) -> None:
        self._client = TestClient(app)

    @staticmethod
    def assert_response_satisfies(
        expected_status_code: int, expected_response: dict, response: JSONResponse
    ):
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))

    async def when_a_post_request_is_sent_to(
        self, endpoint: str, request: dict | None = None
    ) -> JSONResponse:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        request_body.update(request if request else {})
        user_id = UserIdMother.any().value

        with self._client as client:
            return client.post(f"{endpoint}{user_id}", json=request_body)  # type: ignore

    async def given_a_user_is_signed_up(self, user_id: str, request_body: dict) -> None:
        with self._client as client:
            client.post(f"/app/users/{user_id}", json=request_body)

    async def when_a_get_request_is_made_to(
        self, path: str, query_params: dict
    ) -> JSONResponse:
        with self._client as client:
            return client.get(path, params=query_params)  # type: ignore
