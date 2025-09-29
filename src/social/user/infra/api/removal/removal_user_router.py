from fastapi import APIRouter, Depends, Path, status
from starlette.responses import JSONResponse

from src.shared.infra.http.error_response import ResourceNotFoundError
from src.shared.infra.http.success_response import AcceptedResponse
from src.social.user.application.removal.user_removal_command import UserRemovalCommand
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.deps import postgres_user_repository

router = APIRouter()


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
    },
)
async def remove_user(
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    repository: UserRepository = Depends(postgres_user_repository),
) -> JSONResponse:
    command = UserRemovalCommand(user_id=user_id)

    user_remover = UserRemover(repository)
    await user_remover(command)

    return AcceptedResponse(
        data={"message": "User removal request has been accepted."},
    ).as_json()
