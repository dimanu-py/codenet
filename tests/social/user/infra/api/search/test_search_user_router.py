import json

from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestSearchUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_search_user_based_on_filters(self) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(user_id, request_body)
        filter_ = {
            "field": "username",
            "equal": request_body["username"],
        }

        response = await self.when_a_get_request_is_made_to(
            "/app/users/", query_params={"filter": json.dumps(filter_)}
        )

        expected_response = {"users": [{"id": user_id, **request_body}]}
        self.assert_response_satisfies(200, expected_response, response)
