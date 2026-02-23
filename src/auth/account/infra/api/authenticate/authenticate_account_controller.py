from src.auth.account.application.authenticate.account_authenticator import AccountAuthenticator, InvalidCredentials
from src.shared.infra.api.error_response import ErrorResponse, UnauthorizedError
from src.shared.infra.api.success_response import OkResponse, SuccessResponse


class AuthenticateAccountController:
    def __init__(self, use_case: AccountAuthenticator) -> None:
        self._authenticator = use_case

    async def authenticate(self, identification: str, password: str) -> SuccessResponse | ErrorResponse:
        try:
            result = await self._authenticator.execute(identification=identification, password=password)
        except InvalidCredentials as error:
            return UnauthorizedError(error=error.to_primitives())
        return OkResponse(data=result)
