import pytest
from expects import expect, equal
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse

from src.delivery.api.main import app


@pytest.mark.acceptance
@pytest.mark.asyncio
class UserModuleAcceptanceTestConfig:
    def setup_method(self) -> None:
        self._client = TestClient(app)

    @staticmethod
    def assert_response_satisfies(
        expected_status_code: int, expected_response: dict, response: JSONResponse
    ):
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))

    def when_a_post_request_is_sent_to(
        self, endpoint: str, request: dict
    ) -> JSONResponse:
        with self._client as client:
            return client.post(f"{endpoint}", json=request)  # type: ignore

    async def given_a_user_is_signed_up(self, user_id: str, request_body: dict) -> None:
        with self._client as client:
            client.post(f"/users/signup/{user_id}", json=request_body)

    async def when_a_get_request_is_made_to(
        self, path: str, query_params: dict
    ) -> JSONResponse:
        with self._client as client:
            return client.get(path, params=query_params)  # type: ignore
