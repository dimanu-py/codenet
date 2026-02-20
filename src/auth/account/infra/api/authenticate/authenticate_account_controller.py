from src.shared.infra.api.error_response import ErrorResponse
from src.shared.infra.api.success_response import SuccessResponse, OkResponse


class AuthenticateAccountController:
    async def authenticate(self, identification: str, password: str) -> SuccessResponse | ErrorResponse:
        return OkResponse(
            data={
                "access_token": "any",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        )
