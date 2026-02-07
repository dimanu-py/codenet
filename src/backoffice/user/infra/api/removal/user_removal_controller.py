from src.shared.domain.exceptions.application_error import ApplicationError
from src.shared.infra.http.error_response import ErrorResponse, ResourceNotFoundError
from src.shared.infra.http.success_response import AcceptedResponse, SuccessResponse
from src.backoffice.user.application.removal.user_remover import UserRemover


class UserRemovalController:
    def __init__(self, use_case: UserRemover) -> None:
        self._remover = use_case

    async def remove(self, username: str) -> SuccessResponse | ErrorResponse:
        try:
            await self._remover.execute(username)
        except ApplicationError as error:
            return ResourceNotFoundError(error=error.to_primitives())

        return AcceptedResponse()
