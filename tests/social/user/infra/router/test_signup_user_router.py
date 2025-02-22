from src.shared.infra.http.status_code import StatusCode
from tests.social.user.infra.router.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSignupUserRouter(UserModuleAcceptanceTestConfig):
    EMPTY_RESPONSE: dict = {}

    async def test_should_register_a_valid_user(self) -> None:
        response = await self.when_a_post_request_is_sent_to("/users/signup/")

        self.assert_response_satisfies(201, self.EMPTY_RESPONSE, response)

    async def test_should_raise_bad_request_when_name_is_not_valid(self) -> None:
        invalid_name = {
            "name": "John!",
        }
        response = await self.when_a_post_request_is_sent_to("/users/signup/", invalid_name)

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
