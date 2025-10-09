import json

from httpx import AsyncClient
from starlette.responses import JSONResponse

from tests.social.user.domain.mothers.user_email_mother import UserEmailMother
from tests.social.user.domain.mothers.user_id_mother import UserIdMother
from tests.social.user.domain.mothers.user_name_mother import UserNameMother
from tests.social.user.domain.mothers.user_username_mother import UserUsernameMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSearchUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_search_user_based_on_filters(self, client: AsyncClient) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(client, user_id, request_body)
        filter_ = {
            "field": "username",
            "equal": request_body["username"],
        }

        response = await self.when_a_get_request_is_made_to(client, query_params={"filter": json.dumps(filter_)})

        expected_response = {"users": [{"id": user_id, **request_body}]}
        self.assert_response_satisfies(200, expected_response, response)

    async def when_a_get_request_is_made_to(self, client: AsyncClient, query_params: dict) -> JSONResponse:
        return await client.get(self._ROUTE_PATH, params=query_params)  # type: ignore
