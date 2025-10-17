import pytest
from expects import equal, expect
from httpx import AsyncClient
from starlette.responses import JSONResponse


@pytest.mark.asyncio
class UserModuleAcceptanceTestConfig:
    _ROUTE_PATH = "/app/users/"

    @staticmethod
    def assert_response_satisfies(expected_status_code: int, expected_response: dict, response: JSONResponse) -> None:
        expect(response.status_code).to(equal(expected_status_code))
        expect(response.json()).to(equal(expected_response))

    async def given_a_user_is_signed_up(self, client: AsyncClient, user_id: str, request_body: dict) -> None:
        await client.post(f"{self._ROUTE_PATH}{user_id}", json=request_body)
