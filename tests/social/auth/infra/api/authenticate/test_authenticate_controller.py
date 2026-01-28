import pytest


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestAuthenticateController:
    async def test_should_generate_access_token_for_valid_user_credentials(self) -> None: ...
