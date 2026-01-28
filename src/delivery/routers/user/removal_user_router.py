from fastapi import APIRouter, Depends, Path, status
from starlette.responses import JSONResponse

from src.shared.infra.http.error_response import ResourceNotFoundError, UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse
from src.social.user.application.removal.user_remover import UserRemover
from src.social.user.domain.user_repository import UserRepository
from src.delivery.routers.user.deps import postgres_user_repository
from src.social.user.infra.api.removal.user_removal_controller import UserRemovalController

router = APIRouter()


def get_use_case(repository: UserRepository = Depends(postgres_user_repository)) -> UserRemover:
    return UserRemover(repository)


def get_controller(use_case: UserRemover = Depends(get_use_case)):
    return UserRemovalController(use_case)


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
    controller: UserRemovalController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.remove(user_id=user_id)
    return JSONResponse(
        status_code=result.status_code,
        content=result.detail,
    )
