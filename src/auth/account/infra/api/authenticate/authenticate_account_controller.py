from src.shared.infra.api.error_response import ErrorResponse
from src.shared.infra.api.success_response import SuccessResponse


class AuthenticateAccountController:
    async def authenticate(self, identification: str, password: str) -> SuccessResponse | ErrorResponse:
        raise NotImplementedError
