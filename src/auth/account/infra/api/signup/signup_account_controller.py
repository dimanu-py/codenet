from src.auth.account.application.signup.account_signup import AccountSignup
from src.shared.domain.exceptions.domain_error import ConflictError
from src.shared.infra.api.error_response import ConflictErrorResponse, ErrorResponse
from src.shared.infra.api.success_response import AcceptedResponse, SuccessResponse


class SignupAccountController:
    def __init__(self, use_case: AccountSignup) -> None:
        self._signup = use_case

    async def signup(
        self, account_id: str, username: str, email: str, password: str
    ) -> SuccessResponse | ErrorResponse:
        try:
            await self._signup.execute(account_id=account_id, username=username, email=email, plain_password=password)
        except ConflictError as error:
            return ConflictErrorResponse(error=error.to_primitives())
        return AcceptedResponse()
