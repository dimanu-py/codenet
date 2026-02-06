from fastapi import APIRouter, Depends, Path, status
from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse
from src.app.routers.social.user import postgres_user_repository

from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.http.error_response import UnprocessableEntityError
from src.shared.infra.http.success_response import AcceptedResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.delivery.signup.signup_request import SignupRequest
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.signup.user_signup_controller import UserSignupController

router = APIRouter()


def get_controller(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSignupController:
    return UserSignupController(use_case=UserSignup(repository))


@router.post(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def signup_user(
    request: SignupRequest,
    user_id: str = Path(..., openapi_examples={"valid_id": Example(value="123e4567-e89b-12d3-a456-426614174000")}),
    controller: UserSignupController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.signup(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
    )
    return FastAPIResponse.as_json(result)
