from sindripy.value_objects import SindriValidationError

from src.shared.domain.exceptions.application_error import ApplicationError
from src.shared.infra.http.error_response import UnprocessableEntityError, ResourceNotFoundError, ErrorResponse
from src.shared.infra.http.success_response import AcceptedResponse, SuccessResponse
from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.application.removal.user_remover import UserRemover


class UserRemovalController:
    def __init__(self, use_case: UserRemover) -> None:
        self._remover = use_case

    async def remove(self, user_id: str) -> SuccessResponse | ErrorResponse:
        command = UserRemovalCommand(user_id=user_id)

        try:
            await self._remover.execute(command)
        except SindriValidationError as domain_error:
            return UnprocessableEntityError(detail={"message": domain_error.message})
        except ApplicationError as application_error:
            return ResourceNotFoundError(detail={"message": application_error.message})

        return AcceptedResponse(
            detail={"message": "User removal request has been accepted."},
        )
