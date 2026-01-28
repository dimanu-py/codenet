from sindripy.value_objects import SindriValidationError

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.error_response import UnprocessableEntityError, ErrorResponse
from src.shared.infra.http.success_response import CreatedResponse, SuccessResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand


class UserSignupController:
    def __init__(self, use_case: UserSignup) -> None:
        self._signup = use_case

    async def signup(self, id: str, name: str, username: str, email: str, password: str) -> SuccessResponse | ErrorResponse:
        command = UserSignupCommand(
            id=id,
            name=name,
            username=username,
            email=email,
            password=password,
        )

        try:
            await self._signup.execute(command)
        except (DomainError, SindriValidationError) as domain_error:
            return UnprocessableEntityError(detail={"message": domain_error.message})

        return CreatedResponse(
            detail={"resource": f"/app/users/{id}"},
        )