from httpx import AsyncClient
from starlette.responses import JSONResponse

from tests.social.user.domain.mothers.user_email_mother import UserEmailMother
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.domain.mothers.user_name_mother import UserNameMother
from tests.social.user.domain.mothers.user_username_mother import UserUsernameMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSignupUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_register_a_valid_user(self, client: AsyncClient) -> None:
        response = await self.when_a_post_request_is_sent(client)

        expected_id_request = str(response.request.url).split("/")[-1]
        self.assert_response_satisfies(201, {"resource": f"{self._ROUTE_PATH}{expected_id_request}"}, response)

    async def test_should_raise_bad_request_when_name_is_not_valid(self, client: AsyncClient) -> None:
        invalid_name = {
            "name": "John!",
        }
        response = await self.when_a_post_request_is_sent(client, invalid_name)

        self.assert_response_satisfies(
            422,
            {"detail": "Name cannot contain special characters or numbers."},
            response,
        )

    async def when_a_post_request_is_sent(self, client: AsyncClient, request: dict | None = None) -> JSONResponse:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        request_body.update(request if request else {})
        user_id = UserIdMother.any().value

        return await client.post(f"{self._ROUTE_PATH}{user_id}", json=request_body)  # type: ignore
