from src.shared.domain.exceptions.application_error import ConflictError
from src.shared.domain.exceptions.domain_validation_error import DomainValidationError
from src.shared.infra.http.error_response import ConflictErrorResponse, ErrorResponse, UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse, SuccessResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand


class UserSignupController:
    def __init__(self, use_case: UserSignup) -> None:
        self._signup = use_case

    async def signup(
        self, id: str, name: str, username: str, email: str
    ) -> SuccessResponse | ErrorResponse:
        command = UserSignupCommand(
            id=id,
            name=name,
            username=username,
            email=email,
        )

        try:
            await self._signup.execute(command)
        except DomainValidationError as error:
            return UnprocessableEntityError(error=error.to_primitives())
        except ConflictError as error:
            return ConflictErrorResponse(error=error.to_primitives())

        return AcceptedResponse()
