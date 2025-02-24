import json

from tests.delivery.api.user.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)
from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother


class TestSearchUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_search_user_based_on_filters(self) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(user_id, request_body)
        filters = [
            {"field": "username", "operator": "eq", "value": request_body["username"]}
        ]

        response = await self.when_a_get_request_is_made_to(
            "/users/search/", query_params={"filters": json.dumps(filters)}
        )

        expected_response = {"users": [{"id": user_id, **request_body}]}
        self.assert_response_satisfies(200, expected_response, response)
