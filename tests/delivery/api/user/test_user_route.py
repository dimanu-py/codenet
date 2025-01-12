import pytest
from expects import expect, equal
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from src.delivery.api.main import app


@pytest.mark.acceptance
class TestUserRoute:
    NO_BODY: dict = {}

    def setup_method(self) -> None:
        self._client = TestClient(app)

    def test_should_register_a_valid_user(self) -> None:
        request_body = {
            "name": "Dimanu",
            "username": "dimanu",
            "email": "dimanu@py.com",
            "profile_picture": "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        }
        user_id = "2827970-f484-48a2-abd2-aa8f205b295a"

        response = self.when_a_put_request_is_made_to(f"/users/{user_id}", request_body)

        self.then_response_should_satisfy(201, self.NO_BODY, response)

    def when_a_put_request_is_made_to(
        self, endpoint: str, request_body: dict
    ) -> JSONResponse:
        return self._client.put(endpoint, json=request_body)  # type: ignore

    def then_response_should_satisfy(
        self, expected_status_code: int, expected_body: dict, response: JSONResponse
    ) -> None:
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_body))
