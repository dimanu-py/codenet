from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.backoffice.user.infra.api.removal.user_removal_controller import UserRemovalController
from src.shared.delivery.api_parameter import ApiDocExample, PathParameter
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import ResourceNotFoundError, UnprocessableEntityError
from src.shared.infra.api.success_response import AcceptedResponse

router = APIRouter()

UsernamePathParameter = Annotated[
    str,
    PathParameter(description="Username", examples=[ApiDocExample(name="valid_username", value="johndoe")]),
]


@router.delete(
    "/{user_username}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
@inject
async def remove_user(
    user_username: UsernamePathParameter,
    controller: FromDishka[UserRemovalController],
) -> JSONResponse:
    result = await controller.remove(username=user_username)
    return FastAPIResponse.as_json(result)
