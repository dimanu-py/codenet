from starlette.responses import JSONResponse

from tests.social.user.domain.user_email_mother import UserEmailMother
from tests.social.user.domain.user_id_mother import UserIdMother
from tests.social.user.domain.user_name_mother import UserNameMother
from tests.social.user.domain.user_username_mother import UserUsernameMother
from tests.social.user.infra.api.user_module_acceptance_test_config import (
    UserModuleAcceptanceTestConfig,
)


class TestRemovalUserRouter(UserModuleAcceptanceTestConfig):
    async def test_should_remove_existing_user(self) -> None:
        request_body = {
            "name": UserNameMother.any().value,
            "username": UserUsernameMother.any().value,
            "email": UserEmailMother.any().value,
        }
        user_id = UserIdMother.any().value
        await self.given_a_user_is_signed_up(user_id, request_body)

        response = await self.when_a_delete_request_is_sent_to(
            "/users/removal/", user_id
        )

        self.assert_response_satisfies(202, self.EMPTY_RESPONSE, response)

    async def when_a_delete_request_is_sent_to(
        self, endpoint: str, user_id: str
    ) -> JSONResponse:
        with self._client as client:
            return client.delete(f"{endpoint}{user_id}")  # type: ignore
