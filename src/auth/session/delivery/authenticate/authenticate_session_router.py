from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.session.infra.api.authenticate.authenticate_session_controller import AuthenticateSessionController
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import UnauthorizedError, UnprocessableEntityError
from src.shared.infra.api.success_response import OkResponse

authenticate_session_router = APIRouter()


@authenticate_session_router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)
@inject
async def authenticate_session(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: FromDishka[AuthenticateSessionController],
) -> JSONResponse:
    result = await controller.authenticate(
        identification=login_form.username,
        password=login_form.password,
    )
    return FastAPIResponse.as_json(result)
