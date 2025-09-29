from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSignupUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_register_a_valid_user(self) -> None:
        response = await self.when_a_post_request_is_sent_to("/app/users/")

        expected_id_request = str(response.request.url).split("/")[-1]
        self.assert_response_satisfies(201, {"resource": f"/app/users/{expected_id_request}"}, response)

    async def test_should_raise_bad_request_when_name_is_not_valid(self) -> None:
        invalid_name = {
            "name": "John!",
        }
        response = await self.when_a_post_request_is_sent_to("/app/users/", invalid_name)

        self.assert_response_satisfies(
            422,
            {"detail": "Name cannot contain special characters or numbers."},
            response,
        )
