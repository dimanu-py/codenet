from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.backoffice.user.application.removal.user_remover import UserRemover
from src.backoffice.user.delivery.deps import postgres_user_repository
from src.backoffice.user.domain.user_repository import UserRepository
from src.backoffice.user.infra.api.removal.user_removal_controller import UserRemovalController
from src.shared.delivery.api_parameter import PathParameter, ApiDocExample
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import ResourceNotFoundError, UnprocessableEntityError
from src.shared.infra.api.success_response import AcceptedResponse

router = APIRouter()

UsernamePathParameter = Annotated[
    str,
    PathParameter(description="Username", examples=[ApiDocExample(name="valid_username", value="johndoe")]),
]


def get_controller(repository: UserRepository = Depends(postgres_user_repository)) -> UserRemovalController:
    return UserRemovalController(use_case=UserRemover(repository))


@router.delete(
    "/{user_username}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def remove_user(
    user_username: UsernamePathParameter,
    controller: UserRemovalController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.remove(username=user_username)
    return FastAPIResponse.as_json(result)
