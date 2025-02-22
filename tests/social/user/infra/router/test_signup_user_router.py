from src.shared.infra.http.status_code import StatusCode
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother
from tests.social.user.infra.router.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSignupUserRouter(UserModuleAcceptanceTestConfig):
    EMPTY_RESPONSE: dict = {}

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
