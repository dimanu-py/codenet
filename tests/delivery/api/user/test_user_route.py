import pytest

from tests.contexts.social.user.domain.user_email_mother import UserEmailMother
from tests.contexts.social.user.domain.user_id_mother import UserIdMother
from tests.contexts.social.user.domain.user_name_mother import UserNameMother
from tests.contexts.social.user.domain.user_profile_picture_mother import (
    UserProfilePictureMother,
)
from tests.contexts.social.user.domain.user_username_mother import UserUsernameMother
from tests.delivery.api.acceptance_test_config import AcceptanceTestConfig


class TestUserRoute(AcceptanceTestConfig):
    NO_BODY: dict = {}

    def setup_method(self) -> None:
        super().setup_method()
        self.request_body = {
            "name": UserNameMother.create().value,
            "username": UserUsernameMother.create().value,
            "email": UserEmailMother.create().value,
            "profile_picture": UserProfilePictureMother.create().value,
        }
        self.request_user_id = UserIdMother.create().value

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        response = await self.when_a_put_request_is_made_to(
            f"/users/{self.request_user_id}", self.request_body
        )

        self.then_response_should_satisfy(201, self.NO_BODY, response)

    @pytest.mark.asyncio
    async def test_should_unregister_an_existing_user(self) -> None:
        await self.given_a_user_is_registered(self.request_user_id, self.request_body)

        response = await self.when_a_delete_request_is_made_to(
            f"/users/{self.request_user_id}"
        )

        self.then_response_should_satisfy(204, self.NO_BODY, response)

    async def given_a_user_is_registered(
        self, user_id: str, user_request: dict
    ) -> None:
        await self.when_a_put_request_is_made_to(f"/users/{user_id}", user_request)
