from httpx import AsyncClient
from starlette.responses import JSONResponse

from tests.social.user.domain.mothers.user_email_mother import UserEmailMother
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.domain.mothers.user_name_mother import UserNameMother
from tests.social.user.domain.mothers.user_username_mother import UserUsernameMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestRemovalUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_remove_existing_user(self, client: AsyncClient) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(client, user_id, request_body)

        response = await self.when_a_delete_request_is_sent(client, user_id)

        self.assert_response_satisfies(202, {"message": "User removal request has been accepted."}, response)

    async def when_a_delete_request_is_sent(self, client: AsyncClient, user_id: str) -> JSONResponse:
        return await client.delete(f"{self._ROUTE_PATH}{user_id}")  # type: ignore
