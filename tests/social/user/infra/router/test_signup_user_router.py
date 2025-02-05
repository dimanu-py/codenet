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
class TestSignupUserRouter:
    EMPTY_RESPONSE: dict = {}

    def setup_method(self) -> None:
        self._client = TestClient(app)

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        response = self.when_a_post_request_is_sent_to("/users/signup")

        self.assert_response_satisfies(201, self.EMPTY_RESPONSE, response)

    @staticmethod
    def assert_response_satisfies(
        expected_status_code: int, expected_response: dict, response: JSONResponse
    ):
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))

    def when_a_post_request_is_sent_to(self, endpoint: str) -> JSONResponse:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value

        return self._client.post(f"{endpoint}/{user_id}", json=request_body)  # type: ignore
