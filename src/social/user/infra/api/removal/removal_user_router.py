from fastapi import APIRouter, Depends, Path, status
from sindripy.value_objects import SindriValidationError
from starlette.responses import JSONResponse

from src.shared.domain.exceptions.application_error import ApplicationError
from src.shared.infra.http.error_response import ResourceNotFoundError, UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse
from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository

router = APIRouter()


def user_remover_use_case(repository: UserRepository = Depends(postgres_user_repository)) -> UserRemover:
    return UserRemover(repository)


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": UnprocessableEntityError},
    },
)
async def remove_user(
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    user_remover: UserRemover = Depends(user_remover_use_case),
) -> JSONResponse:
    command = UserRemovalCommand(user_id=user_id)

    try:
        await user_remover.execute(command)
    except SindriValidationError as domain_error:
        return UnprocessableEntityError(detail=domain_error.message).as_json()
    except ApplicationError as application_error:
        return ResourceNotFoundError(detail=application_error.message).as_json()

    return AcceptedResponse(
        data={"message": "User removal request has been accepted."},
    ).as_json()
