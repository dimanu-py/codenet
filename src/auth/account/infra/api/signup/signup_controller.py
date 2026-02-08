from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.shared.domain.exceptions.application_error import ConflictError
from src.shared.infra.http.error_response import ConflictErrorResponse, ErrorResponse
from src.shared.infra.http.success_response import AcceptedResponse, SuccessResponse


class SignupController:
    def __init__(self, use_case: AccountWithUserSignup) -> None:
        self._signup = use_case

    async def signup(self, account_id: str, name: str, username: str, email: str, password: str) -> SuccessResponse | ErrorResponse:
        try:
            await self._signup.execute(
                account_id=account_id,
                name=name,
                username=username,
                email=email,
                plain_password=password,
            )
        except ConflictError as error:
            return ConflictErrorResponse(error=error.to_primitives())
        return AcceptedResponse()
