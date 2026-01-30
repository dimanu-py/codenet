from sindripy.value_objects import SindriValidationError

from src.shared.domain.exceptions.domain_validation_error import DomainValidationError
from src.shared.infra.http.error_response import ErrorResponse, UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse, SuccessResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.application.signup.user_signup_command import UserSignupCommand


class UserSignupController:
    def __init__(self, use_case: UserSignup) -> None:
        self._signup = use_case

    async def signup(
        self, id: str, name: str, username: str, email: str, password: str
    ) -> SuccessResponse | ErrorResponse:
        command = UserSignupCommand(
            id=id,
            name=name,
            username=username,
            email=email,
            password=password,
        )

        try:
            await self._signup.execute(command)
        except (DomainValidationError, SindriValidationError) as domain_error:
            return UnprocessableEntityError(detail={"message": domain_error.message})

        return AcceptedResponse(detail={"message": "User signup request has been accepted."})
