import pytest
from expects import expect, equal
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from src.delivery.api.main import app
from src.shared.infra.status_code import StatusCode
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
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        response = self.when_a_post_request_is_sent_to(
            f"/users/signup/{user_id}", request_body
        )

        self.assert_response_satisfies(201, self.EMPTY_RESPONSE, response)

    @pytest.mark.asyncio
    async def test_should_raise_bad_request_when_name_is_not_valid(self) -> None:
        request_body = {
            "name": "John!",
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        response = self.when_a_post_request_is_sent_to(
            f"/users/signup/{user_id}", request_body
        )

        self.assert_response_satisfies(
            StatusCode.BAD_REQUEST,
            {
                "error": {
                    "type": "invalid_name_format",
                    "message": "Name cannot contain special characters or numbers.",
                }
            },
            response,
        )

    @staticmethod
    def assert_response_satisfies(
        expected_status_code: int, expected_response: dict, response: JSONResponse
    ):
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))

    def when_a_post_request_is_sent_to(
        self, endpoint: str, request: dict
    ) -> JSONResponse:
        return self._client.post(f"{endpoint}", json=request)  # type: ignore
