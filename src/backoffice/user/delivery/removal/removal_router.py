from fastapi import APIRouter, Depends, Path, status
from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.http.error_response import ResourceNotFoundError, UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse
from src.backoffice.user.application.removal.user_remover import UserRemover
from src.backoffice.user.delivery.deps import postgres_user_repository
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.infra.api.removal.user_removal_controller import UserRemovalController

router = APIRouter()


def get_controller(repository: UserRepository = Depends(postgres_user_repository)) -> UserRemovalController:
    return UserRemovalController(use_case=UserRemover(repository))


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def remove_user(
    user_id: str = Path(..., openapi_examples={"valid_id": Example(value="123e4567-e89b-12d3-a456-426614174000")}),
    controller: UserRemovalController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.remove(username=user_id)
    return FastAPIResponse.as_json(result)
