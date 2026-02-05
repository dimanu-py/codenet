from fastapi import APIRouter, status, Path, Depends
from fastapi.openapi.models import Example
from starlette.responses import JSONResponse

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.auth.account.infra.api.signup.signup_controller import SignupController
from src.delivery.routers.auth.account.signup.signup_request import SignupRequest
from src.delivery.routers.fastapi_response import FastAPIResponse
from src.shared.infra.http.error_response import UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse

signup_router = APIRouter()


def get_controller() -> SignupController:
    return SignupController(use_case=AccountWithUserSignup())


@signup_router.post(
    "/{account_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def signup_account_and_user(
    request: SignupRequest,
    account_id: str = Path(
        openapi_examples={"valid_id": Example(value="123e4567-e89b-12d3-a456-426614174000")},
    ),
    controller: SignupController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.signup()
    return FastAPIResponse.as_json(result)
