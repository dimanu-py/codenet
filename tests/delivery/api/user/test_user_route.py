import pytest

from tests.delivery.api.acceptance_test_config import AcceptanceTestConfig


class TestUserRoute(AcceptanceTestConfig):
    NO_BODY: dict = {}

    @pytest.mark.asyncio
    async def test_should_register_a_valid_user(self) -> None:
        request_body = {
            "name": "Dimanu",
            "username": "dimanu",
            "email": "dimanu@py.com",
            "profile_picture": "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        }
        user_id = "2827970-f484-48a2-abd2-aa8f205b295a"

        response = await self.when_a_put_request_is_made_to(
            f"/users/{user_id}", request_body
        )

        self.then_response_should_satisfy(201, self.NO_BODY, response)

    @pytest.mark.asyncio
    async def test_should_unregister_an_existing_user(self) -> None:
        user_request = {
            "name": "Dimanu",
            "username": "dimanu",
            "email": "dimanu@py.com",
            "profile_picture": "https://my-bucket.s3.us-east-1.amazonaws.com/images/picture.jpg",
        }
        user_id = "2827970-f484-48a2-abd2-aa8f205b295a"
        await self.given_a_user_is_registered(user_id, user_request)

        response = await self.when_a_delete_request_is_made_to(f"/users/{user_id}")

        self.then_response_should_satisfy(204, self.NO_BODY, response)

    async def given_a_user_is_registered(
        self, user_id: str, user_request: dict
    ) -> None:
        await self.when_a_put_request_is_made_to(f"/users/{user_id}", user_request)
