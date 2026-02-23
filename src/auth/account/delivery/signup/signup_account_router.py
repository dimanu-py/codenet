from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from src.auth.account.delivery.signup.signup_account_request import SignupAccountRequest
from src.auth.account.infra.api.signup.signup_account_controller import SignupAccountController
from src.shared.delivery.api_parameter import ApiDocExample, PathParameter
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import UnprocessableEntityError
from src.shared.infra.api.success_response import AcceptedResponse

signup_account_router = APIRouter()

AccountIdPathParameter = Annotated[
    str,
    PathParameter(
        description="Account ID",
        examples=[ApiDocExample(name="valid_id", value="123e4567-e89b-12d3-a456-426614174000")],
    ),
]


@signup_account_router.post(
    "/{account_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
@inject
async def signup_account(
    request: SignupAccountRequest,
    account_id: AccountIdPathParameter,
    controller: FromDishka[SignupAccountController],
) -> JSONResponse:
    result = await controller.signup(
        account_id=account_id, username=request.username, email=request.email, password=request.password
    )
    return FastAPIResponse.as_json(result)
