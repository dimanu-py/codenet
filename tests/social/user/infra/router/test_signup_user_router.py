import pytest

from fastapi.testclient import TestClient
from expects import expect, equal

from src.delivery.api.main import app


@pytest.mark.acceptance
class TestSignupUserRouter:
    NO_BODY: dict = {}

    def setup_method(self) -> None:
        self._client = TestClient(app)

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        request_body = {
            "name": "Dimanu",
            "username": "dimanu",
            "email": "dimanu@py.com",
        }
        user_id = "2827970f-4848-48a2-abd2-aa8f205b295a"

        response = self._client.post(f"/users/signup/{user_id}", json=request_body)

        expect(response.status_code).to(equal(201))
        expect(response.json()).to(equal(self.NO_BODY))
