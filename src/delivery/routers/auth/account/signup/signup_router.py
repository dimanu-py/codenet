from fastapi import APIRouter, status, Path
from fastapi.openapi.models import Example
from starlette.responses import JSONResponse

from src.delivery.routers.auth.account.signup.signup_request import SignupRequest
from src.shared.infra.http.error_response import UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse

signup_router = APIRouter()


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
) -> JSONResponse:
    ...
