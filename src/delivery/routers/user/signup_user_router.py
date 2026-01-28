from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from src.delivery.routers.user.deps import postgres_user_repository
from src.delivery.routers.user.user_sign_up_request import UserSignupRequest
from src.shared.infra.http.error_response import UnprocessableEntityError
from src.shared.infra.http.success_response import CreatedResponse
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.domain.user_repository import UserRepository
from src.social.user.infra.api.signup.user_signup_controller import UserSignupController

router = APIRouter()


def get_use_case(
    repository: UserRepository = Depends(postgres_user_repository),
) -> UserSignup:
    return UserSignup(repository)

def get_controller(
    use_case: UserSignup = Depends(get_use_case),
) -> UserSignupController:
    return UserSignupController(use_case=use_case)


@router.post(
    "/{user_id}",
    responses={
        status.HTTP_201_CREATED: {"model": CreatedResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def signup_user(
    request: UserSignupRequest,
    user_id: str = Path(..., examples=["123e4567-e89b-12d3-a456-426614174000"]),
    controller: UserSignupController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.signup(
        id=user_id,
        name=request.name,
        username=request.username,
        email=request.email,
        password=request.password,
    )
    return JSONResponse(
        status_code=result.status_code,
        content=result.detail,
    )
