from src.auth.session.application.authenticate.session_authenticator import InvalidCredentials, SessionAuthenticator
from src.shared.infra.api.error_response import ErrorResponse, UnauthorizedError
from src.shared.infra.api.success_response import OkResponse, SuccessResponse


class AuthenticateSessionController:
    def __init__(self, use_case: SessionAuthenticator) -> None:
        self._authenticator = use_case

    async def authenticate(self, identification: str, password: str) -> SuccessResponse | ErrorResponse:
        try:
            result = await self._authenticator.execute(identification=identification, password=password)
        except InvalidCredentials as error:
            return UnauthorizedError(error=error.to_primitives())
        return OkResponse(data=result)
