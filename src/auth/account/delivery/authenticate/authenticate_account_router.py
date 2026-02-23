from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.account.infra.api.authenticate.authenticate_account_controller import AuthenticateAccountController
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import UnauthorizedError, UnprocessableEntityError
from src.shared.infra.api.success_response import OkResponse

authenticate_account_router = APIRouter()


@authenticate_account_router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)
@inject
async def authenticate_account(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: FromDishka[AuthenticateAccountController],
) -> JSONResponse:
    result = await controller.authenticate(
        identification=login_form.username,
        password=login_form.password,
    )
    return FastAPIResponse.as_json(result)
