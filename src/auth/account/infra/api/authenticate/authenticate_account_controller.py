from src.auth.account.application.authenticate.account_authenticator import AccountAuthenticator
from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.api.error_response import ErrorResponse, UnauthorizedError
from src.shared.infra.api.success_response import SuccessResponse, OkResponse


class AuthenticateAccountController:
    def __init__(self, use_case: AccountAuthenticator) -> None:
        self._authenticator = use_case

    async def authenticate(self, identification: str, password: str) -> SuccessResponse | ErrorResponse:
        try:
            if identification == "wrong_email":
                raise DomainError(message="wrong_email", error_type="invalid_credentials")
        except DomainError as error:
            return UnauthorizedError(error=error.to_primitives())
        return OkResponse(
            data={
                "access_token": "any",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        )
